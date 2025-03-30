import mysql.connector
from mysql.connector import Error
import pandas as pd
import uuid
import mailer


def getSqlConfiguration(configLocation):
    config = {}
    try:
        with open(configLocation, 'r') as conf:
            for line in conf:
                line = line.strip()
                k, v = line.split("=", 1)
                config[k.strip()] = v
        return config
    except FileNotFoundError:
        print(f"Config file not found at {configLocation}!")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        # print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query, values=()):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query, values)
        # result = cursor.fetchall()
        connection.commit()
        print("Query successful:")
        return cursor
    except Error as err:
        print(f"Error: '{err}'")


def createTables(connection):
    campaignTable = '''
CREATE TABLE IF NOT EXISTS Campaigns (
campaign_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
campaign_name VARCHAR(255) NOT NULL,
campaign_company VARCHAR(255) NOT NULL,
date_created DATE
    );
    '''
    targetTable = '''
CREATE TABLE IF NOT EXISTS Targets (
target_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
target_first VARCHAR(255) NOT NULL,
target_last VARCHAR(255) NOT NULL,
target_email VARCHAR(255) NOT NULL,
target_position VARCHAR(255) NOT NULL,
target_department VARCHAR(255) NOT NULL,
campaign_name VARCHAR(255) NOT NULL,
campaign_id INT NOT NULL,
target_company VARCHAR(255) NOT NULL,
date_created DATE
    );
    '''
    senderTable = '''
CREATE TABLE IF NOT EXISTS Senders (
sender_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
sender_first VARCHAR(255) NOT NULL,
sender_last VARCHAR(255) NOT NULL,
from_email VARCHAR(255) NOT NULL,
mail_from_email VARCHAR(255) NOT NULL,
sender_position VARCHAR(255) NOT NULL,
sender_department VARCHAR(255) NOT NULL,
campaign_name VARCHAR(255) NOT NULL,
campaign_id INT NOT NULL,
sender_company VARCHAR(255) NOT NULL,
date_created DATE
    );
    '''
    sentEmailsTable = '''
CREATE TABLE IF NOT EXISTS Sent_Emails (
email_id VARCHAR(255) NOT NULL PRIMARY KEY,
sender_first VARCHAR(255) NOT NULL,
sender_last VARCHAR(255) NOT NULL,
email_mail_from VARCHAR(255) NOT NULL,
email_from VARCHAR(255) NOT NULL,
target_first VARCHAR(255) NOT NULL,
target_last VARCHAR(255) NOT NULL,
target_email VARCHAR(255) NOT NULL,
campaign_id INT NOT NULL,
time_sent DATETIME
    );
    '''
    emailServersTable = '''
CREATE TABLE IF NOT EXISTS Email_Servers (
server_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
server_name VARCHAR(255) NOT NULL,
server_host VARCHAR(255) NOT NULL,
server_port VARCHAR(255) NOT NULL,
server_user VARCHAR(255) NOT NULL,
server_password VARCHAR(255) NOT NULL
    );
    '''

    phished = '''
CREATE TABLE IF NOT EXISTS phished (
phished_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
email_id VARCHAR(255) UNIQUE,
campaign_id INT NOT NULL,
connection_ip VARCHAR(255) NOT NULL,
browser_user_agent VARCHAR(255) NOT NULL,
url VARCHAR(255) NOT NULL,
time DATETIME NOT NULL,
data_submitted BOOLEAN DEFAULT 0
    );
    '''
    execute_query(connection, campaignTable)
    execute_query(connection, targetTable)
    execute_query(connection, senderTable)
    execute_query(connection, sentEmailsTable)
    execute_query(connection, emailServersTable)
    execute_query(connection, phished)


def addEmailServer(connection, serverName, configLocation):
    config = {}
    try:
        with open(configLocation, 'r') as conf:
            for line in conf:
                line = line.strip()
                k, v = line.split("=", 1)
                config[k.strip()] = v
    except FileNotFoundError:
        print(f"Config file not found at {configLocation}!")
    query = """
    INSERT INTO Email_Servers (server_name, server_host, server_port, server_user, server_password)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (serverName, config['HOST'], config['PORT'], config['USERNAME_SMTP'], config['PASSWORD_SMTP'])
    execute_query(connection, query, values)


def addCampaign(connection, campaignName, campaignCompany):
    query = """
    INSERT INTO Campaigns (campaign_name, campaign_company, date_created)
    VALUES (%s, %s, NOW())
    """
    values = (campaignName, campaignCompany)
    execute_query(connection, query, values)


def getCampaignInfo(connection, campaign_id):
    query = "SELECT campaign_name, campaign_company FROM Campaigns where campaign_id = %s"
    campaign = execute_query(connection, query, (campaign_id,)).fetchone()
    if not campaign:
        print(f"Could not retrive campaign {campaign_id}")
    return (campaign[0], campaign[1])


def addTarget(connection, targetFirst, targetLast, targetEmail, targetPosition, targetDepartment, campaignId):
    query = """
    INSERT INTO Targets (target_first, target_last, target_email, target_position, target_department, campaign_name, campaign_id, target_company, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    campaignInfo = getCampaignInfo(connection, campaignId)
    values = (targetFirst, targetLast, targetEmail, targetPosition, targetDepartment, campaignInfo[0], campaignId, campaignInfo[1])
    execute_query(connection, query, values)


def addTargetsCSV(connection, file, campaignId):
    '''
    csvfile format: first,last,email,position,department
    '''

    csv_data = pd.read_csv(file)

    for _, row in csv_data.iterrows():
        addTarget(connection, row['first'], row['last'], row['email'], row['position'], row['department'], campaignId)


def addSender(connection, senderFirst, senderLast, fromEmail, mailFromEmail, senderPosition, senderDepartment, campaignId):
    query = """
    INSERT INTO Senders (sender_first, sender_last, from_email, mail_from_email, sender_position, sender_department, campaign_name, campaign_id, sender_company, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    campaignInfo = getCampaignInfo(connection, campaignId)
    values = (senderFirst, senderLast, fromEmail, mailFromEmail, senderPosition, senderDepartment, campaignInfo[0], campaignId, campaignInfo[1])
    print(values)
    execute_query(connection, query, values)


def addSendersCSV(connection, file, campaignId):
    '''
    csvfile format first,last,email,mail_from,position,department
    '''

    csv_data = pd.read_csv(file)

    for _, row in csv_data.iterrows():
        addSender(connection, row['first'], row['last'], row['email'], row['mail_from'], row['position'], row['department'], campaignId)


def addSentEmail(connection, senderFirst, senderLast, emailMailFrom, emailFrom, targetFirst, targetLast, targetEmail, campaignId):
    query = """
    INSERT INTO Sent_Emails (email_id, sender_first, sender_last, email_mail_from, email_from, target_first, target_last, target_email, campaign_id, time_sent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    uniqueID = str(uuid.uuid4())
    values = (uniqueID, senderFirst, senderLast, emailMailFrom, emailFrom, targetFirst, targetLast, targetEmail, campaignId)
    execute_query(connection, query, values)
    return uniqueID


def deleteCampaignById(connection, campaign_id):
    tables = ['Campaigns', 'Targets', 'Senders', 'Sent_Emails']
    for table in tables:
        query = f"DELETE FROM {table} WHERE campaign_id = %s"
        execute_query(connection, query, (campaign_id,))


def deleteTargetById(connection, target_id):
    query = "DELETE FROM Targets WHERE target_id = %s"
    execute_query(connection, query, (target_id,))


def deleteSenderById(connection, sender_id):
    query = "DELETE FROM Senders WHERE sender_id = %s"
    execute_query(connection, query, (sender_id,))


def deleteSentEmailById(connection, email_id):
    query = "DELETE FROM Sent_Emails WHERE email_id = %s"
    execute_query(connection, query, (email_id,))


def deleteServerById(connection, server_id):
    query = "DELETE FROM Email_Servers WHERE server_id = %s"
    execute_query(connection, query, (server_id,))


def deletePhishedById(connection, phished_id):
    query = "DELETE FROM phished WHERE phished_id = %s"
    execute_query(connection, query, (phished_id,))


def displayTable(connection, table):
    query = f"SELECT * FROM {table}"
    cursor = execute_query(connection, query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    print(df.to_string(index=False))


def displayTableByCampaign(connection, table, campaignId):
    query = f"SELECT * FROM {table} WHERE campaign_id = %s"
    cursor = execute_query(connection, query, (campaignId,))
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    print(df.to_string(index=False))


def sendEmailByCampaign(connection, campaignId, senderId, serverId, subject, template):
    targetsQuery = "SELECT target_first, target_last, target_email, target_position, target_department FROM Targets where campaign_id = %s;"
    targets = execute_query(connection, targetsQuery, (campaignId,)).fetchall()
    senderQuery = "SELECT sender_first, sender_last, from_email, mail_from_email, sender_position, sender_department FROM Senders where sender_id = %s;"
    sender = execute_query(connection, senderQuery, (senderId,)).fetchone()
    serverQuery = "SELECT server_host, server_port, server_user, server_password FROM Email_Servers WHERE server_id = %s"
    server = execute_query(connection, serverQuery, (serverId,)).fetchone()

    server_conf = {
        'HOST': server[0],
        'PORT': server[1],
        'USERNAME_SMTP': server[2],
        'PASSWORD_SMTP': server[3]
    }

    emailHeaders = {
        'SENDERFIRST': sender[0],
        'SENDERLAST': sender[1],
        'SENDERNAME': f'{sender[0]} {sender[1]}',
        'SENDER': sender[3],
        'SPOOFED': sender[2],
        'SENDERPOSITION': sender[4],
        'SENDERDEPARTMENT': sender[5],
        'SUBJECT': subject
    }

    template = mailer.getEmailTemplate(template)
    for target in targets:
        emailHeaders['RECIPIENT'] = target[2]
        emailHeaders['RECIPIENTFIRST'] = target[0]
        emailHeaders['RECIPIENTLAST'] = target[1]
        emailHeaders['RECIPIENTNAME'] = f"{target[0]} {target[1]}"
        emailHeaders['RECIPIENTPOSITION'] = target[3]
        emailHeaders['RECIPIENTDEPARTMENT'] = target[4]
        emailHeaders['uuid'] = addSentEmail(connection, sender[0], sender[1], sender[3], sender[2], target[0], target[1], target[2], campaignId)
        mailer.sendEmail(emailHeaders, server_conf, template)
