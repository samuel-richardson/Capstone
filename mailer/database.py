import mysql.connector
from mysql.connector import Error
import pandas as pd


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
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query, values=()):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
        print("Query successful")
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
target_phone VARCHAR(255),
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
sender_phone VARCHAR(20),
campaign_name VARCHAR(255) NOT NULL,
campaign_id INT NOT NULL,
sender_company VARCHAR(255) NOT NULL,
date_created DATE
    );
    '''
    sentEmailsTable = '''
CREATE TABLE Sent_Emails (
id INT AUTO_INCREMENT PRIMARY KEY,
sender_first VARCHAR(255),
sender_last VARCHAR(255),
email_mail_from VARCHAR(255),
email_from VARCHAR(255),
target_first VARCHAR(255),
target_last VARCHAR(255),
target_email VARCHAR(255),
time_sent DATETIME 
);
    ''' 
    execute_query(connection, campaignTable)
    execute_query(connection, targetTable)
    execute_query(connection, senderTable)
    execute_query(connection, sentEmailsTable)


def addCampaign(connection, campaignName, campaignCompany):
    query = """
    INSERT INTO Campaigns (campaign_name, campaign_company, date_created)
    VALUES (%s, %s, NOW())
    """
    values = (campaignName, campaignCompany)
    execute_query(connection, query, values)


def addTarget(connection, targetFirst, targetLast, targetEmail, targetPosition, targetDepartment, targetPhone, campaignName, campaignId, targetCompany):
    query = """
    INSERT INTO Targets (target_first, target_last, target_email, target_position, target_department, target_phone, campaign_name, campaign_id, target_company, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    values = (targetFirst, targetLast, targetEmail, targetPosition, targetDepartment, targetPhone, campaignName, campaignId, targetCompany)
    execute_query(connection, query, values)


def addSender(connection, senderFirst, senderLast, fromEmail, mailFromEmail, senderPosition, senderDepartment, campaignName, campaignId, senderCompany, senderPhone=None):
    query = """
    INSERT INTO Senders (sender_first, sender_last, from_email, mail_from_email, sender_position, sender_department, sender_phone, campaign_name, campaign_id, sender_company, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    values = (senderFirst, senderLast, fromEmail, mailFromEmail, senderPosition, senderDepartment, senderPhone, campaignName, campaignId, senderCompany)
    execute_query(connection, query, values)


def addSentEmail(connection, senderFirst, senderLast, emailMailFrom, emailFrom, targetFirst, targetLast, targetEmail):
    query = """
    INSERT INTO Sent_Emails (sender_first, sender_last, email_mail_from, email_from, target_first, target_last, target_email, time_sent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """
    values = (senderFirst, senderLast, emailMailFrom, emailFrom, targetFirst, targetLast, targetEmail)
    execute_query(connection, query, values)


def deleteCampaign(connection, campaign_id):
    query = "DELETE FROM Campaigns WHERE campaign_id = %s"
    execute_query(connection, query, (campaign_id,))


def deleteTarget(connection, target_id):
    query = "DELETE FROM Targets WHERE target_id = %s"
    execute_query(connection, query, (target_id,))


def deleteSender(connection, sender_id):
    query = "DELETE FROM Senders WHERE sender_id = %s"
    execute_query(connection, query, (sender_id,))


def deleteSentEmail(connection, email_id):
    query = "DELETE FROM communication WHERE id = %s"
    execute_query(connection, query, (email_id,))


