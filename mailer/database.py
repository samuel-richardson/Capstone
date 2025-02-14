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


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, query):
    # CREATE DATABASE IF NOT EXISTS DBName;
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


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


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def createTables(connection):
    campaignTable = '''
CREATE TABLE Campaigns (
campaign_id INT NOT NULL AUTO_INCRAMENT PRIMARY KEY,
campaign_name VARCHAR(255) NOT NULL,
campaign_company VARCHAR(255) NOT NULL,
date_created DATE
);
    '''
    targetTable = '''
CREATE TABLE Targets (
target_id INT NOT NULL AUTO_INCRAMENT PRIMARY KEY,
target_first VARCHAR(255) NOT NULL,
target_last VARCHAR(255) NOT NULL,
target_email VARCHAR(255) NOT NULL,
target_phone VARCHAR(255),
campaign_name VARCHAR(255) NOT NULL,
campaign_id INT NOT NULL,
target_company VARCHAR(255) NOT NULL,
date_created DATE
    );
    '''
    senderTable = '''
CREATE TABLE Senders (
sender_id INT NOT NULL AUTO_INCRAMENT PRIMARY KEY,
sender_first VARCHAR(255) NOT NULL,
sender_last VARCHAR(255) NOT NULL,
from_email VARCHAR(255) NOT NULL,
alt_from_email VARCHAR(255) NOT NULL,
mail_from_email VARCHAR(255) NOT NULL,
alt_mail_from_email VARCHAR(255) NOT NULL,
sender_phone VARCHAR(20),
campaign_name VARCHAR(255) NOT NULL,
campaign_id INT NOT NULL,
sender_company VARCHAR(255) NOT NULL,
date_created DATE
    );
    '''
    sentEmailsTable = '''
CREATE TABLE communication (
id INT AUTO_INCREMENT PRIMARY KEY,
sender_id INT,
target_id INT,
sender_first VARCHAR(255),
sender_last VARCHAR(255),
mail_from_email VARCHAR(255),
email_from VARCHAR(255),
target_first VARCHAR(255),
target_last VARCHAR(255),
target_email VARCHAR(255),
time_sent DATETIME 
);
    ''' 
