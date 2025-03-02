import mysql.connector
from mysql.connector import Error
import pandas as pd
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
    cursor = connection.cursor()
    try:
        result = cursor.execute(query, values)
        result = result.fetchone()
        connection.commit()
        print("Query successful:")
        return result
    except Error as err:
        print(f"Error: '{err}'")


def createTables(connection):
    campaignTable = '''
CREATE TABLE Campaigns (
campaign_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
campaign_name VARCHAR(255) NOT NULL,
campaign_company VARCHAR(255) NOT NULL,
date_created DATE
    );
    '''
    targetTable = '''
CREATE TABLE Targets (
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
CREATE TABLE Senders (
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
CREATE TABLE Sent_Emails (
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
CREATE TABLE Email_Servers (
server_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
server_name VARCHAR(255) NOT NULL,
server_host VARCHAR(255) NOT NULL,
server_port VARCHAR(255) NOT NULL,
server_user VARCHAR(255) NOT NULL,
server_password VARCHAR(255) NOT NULL
    );
    '''
    execute_query(connection, campaignTable)
    execute_query(connection, targetTable)
    execute_query(connection, senderTable)
    execute_query(connection, sentEmailsTable)
    execute_query(connection, emailServersTable)


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


def addTarget(connection, targetFirst, targetLast, targetEmail, targetPosition, targetDepartment, campaignName, campaignId, targetCompany):
    query = """
    INSERT INTO Targets (target_first, target_last, target_email, target_position, target_department, campaign_name, campaign_id, target_company, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    values = (targetFirst, targetLast, targetEmail, targetPosition, targetDepartment, campaignName, campaignId, targetCompany)
    execute_query(connection, query, values)


def addTargetsCSV(connection, file, campaignId):
    '''
    csvfile format first,last,email,position,department
    '''

    campaignQuery = "SELECT campaign_name, campaign_company FROM Campaigns where campaign_id = %s"
    campaignResults = execute_query(connection, campaignQuery, (campaignId,))

    if not campaignResults:
        print("Could not retrive the selected campaign!")
        return

    campaignName, campaignCompany = campaignResults[0], campaignResults[1]

    csv_data = pd.read_csv(file)

    for _,row in csv_data.iterrows():
        addTarget(connection, row['first'], row['last'], row['email'], row['position'], row['department'], campaignName, campaignId, campaignCompany)


def addSender(connection, senderFirst, senderLast, fromEmail, mailFromEmail, senderPosition,
              senderDepartment, campaignName, campaignId, senderCompany):
    query = """
    INSERT INTO Senders (sender_first, sender_last, from_email, mail_from_email, sender_position, sender_department, campaign_name, campaign_id, sender_company, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    values = (senderFirst, senderLast, fromEmail, mailFromEmail, senderPosition, senderDepartment, campaignName, campaignId, senderCompany)
    execute_query(connection, query, values)


def addSendersCSV(connection, file, campaignId):
    '''
    csvfile format first,last,email,mail_from,position,department
    '''

    campaignQuery = "SELECT campaign_name, campaign_company FROM Campaigns where campaign_id = %s"
    campaignResults = execute_query(connection, campaignQuery, (campaignId,))

    if not campaignResults:
        print("Could not retrive the selected campaign!")
        return

    campaignName, campaignCompany = campaignResults[0], campaignResults[1]

    csv_data = pd.read_csv(file)

    for _, row in csv_data.iterrows():
        addTarget(connection, row['first'], row['last'], row['email'], row['mail_from'], row['position'], row['department'], campaignName, campaignId, campaignCompany)


def addSentEmail(connection, senderFirst, senderLast, emailMailFrom, emailFrom, targetFirst, targetLast, targetEmail, campaignId):
    query = """
    INSERT INTO Sent_Emails (email_id, sender_first, sender_last, email_mail_from, email_from, target_first, target_last, target_email, time_sent)
    VALUES (UUID(), %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    values = (senderFirst, senderLast, emailMailFrom, emailFrom, targetFirst, targetLast, campaignId)
    execute_query(connection, query, values)
    uuidQuery = "select last_insert_uuid();"
    uuid = execute_query(connection, uuidQuery)
    return uuid


def deleteCampaignById(connection, campaign_id):
    query = "DELETE FROM Campaigns WHERE campaign_id = %s"
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


def displayTable(connection, table):
    result = pd.read_sql(connection, table)
    print(result.to_string())


def listTables(connection):
    query = "SHOW TABLES;"
    result = pd.read_sql(connection, query)
    print(result.to_string())

def sendEmailByCampaign(connection, campaignId, senderId, serverId):
    targetsQuery = "SELECT target_first, target_last, target_email, target_position, target_department FROM Targets where campaign_id = %s;"
    targets = execute_query(connection, targetsQuery, (campaignId,))
    senderQuery = "SELECT sender_first, sender_last, from_email, mail_from_email, sender_position, sender_department where campaign_id = %s;"
    sender = execute_query(connection, senderQuery, (senderId,))
    serverQuery = "SELECT server_host, server_port, server_user, server_password FROM Email_Servers WHERE server_id = %s"
    server = execute_query(connection, serverQuery, (serverId,))

    print(targetsQuery)
    print(senderQuery)
    print(serverQuery)


