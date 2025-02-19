import unittest
import mysql.connector
from database import (
    getSqlConfiguration,
    create_db_connection,
    createTables,
    addCampaign,
    addTarget,
    addSender,
    addSentEmail,
    deleteCampaign,
    deleteTarget,
    deleteSender,
    deleteSentEmail
)

CONFIG_FILE = "dbconfig.txt"  # Ensure this file contains valid database credentials.

class TestDatabaseFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the database connection and create tables before running tests."""
        config = getSqlConfiguration(CONFIG_FILE)
        cls.host = config.get("HOST")
        cls.user = config.get("USER")
        cls.password = config.get("PASSWORD")
        cls.database = config.get("DATABASE")

        cls.connection = create_db_connection(cls.host, cls.user, cls.password, cls.database)
        createTables(cls.connection)  # Ensure tables exist before testing

    def test_campaign_operations(self):
        """Test adding and deleting a campaign."""
        addCampaign(self.connection, "Security Awareness", "CyberCorp")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Campaigns WHERE campaign_name = %s", ("Security Awareness",))
        campaign = cursor.fetchone()
        self.assertIsNotNone(campaign, "Campaign was not inserted")

        deleteCampaign(self.connection, campaign[0])

        cursor.execute("SELECT * FROM Campaigns WHERE campaign_name = %s", ("Security Awareness",))
        self.assertIsNone(cursor.fetchone(), "Campaign was not deleted")

    def test_target_operations(self):
        """Test adding and deleting a target."""
        addTarget(self.connection, "John", "Doe", "john.doe@example.com", "Analyst", "IT", "Security Awareness", 1, "CyberCorp")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Targets WHERE target_email = %s", ("john.doe@example.com",))
        target = cursor.fetchone()
        self.assertIsNotNone(target, "Target was not inserted")

        deleteTarget(self.connection, target[0])

        cursor.execute("SELECT * FROM Targets WHERE target_email = %s", ("john.doe@example.com",))
        self.assertIsNone(cursor.fetchone(), "Target was not deleted")

    def test_sender_operations(self):
        """Test adding and deleting a sender."""
        addSender(self.connection, "Alice", "Smith", "alice@example.com", "mail@example.com", "Manager", "Security", "Security Awareness", 1, "CyberCorp")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Senders WHERE from_email = %s", ("alice@example.com",))
        sender = cursor.fetchone()
        self.assertIsNotNone(sender, "Sender was not inserted")

        deleteSender(self.connection, sender[0])

        cursor.execute("SELECT * FROM Senders WHERE from_email = %s", ("alice@example.com",))
        self.assertIsNone(cursor.fetchone(), "Sender was not deleted")

    def test_sent_email_operations(self):
        """Test adding and deleting a sent email record."""
        addSentEmail(self.connection, "Alice", "Smith", "mail@example.com", "alice@example.com", "John", "Doe", "john.doe@example.com")

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Sent_Emails WHERE target_email = %s", ("john.doe@example.com",))
        sent_email = cursor.fetchone()
        self.assertIsNotNone(sent_email, "Sent email record was not inserted")

        deleteSentEmail(self.connection, sent_email[0])

        cursor.execute("SELECT * FROM Sent_Emails WHERE target_email = %s", ("john.doe@example.com",))
        self.assertIsNone(cursor.fetchone(), "Sent email record was not deleted")

    @classmethod
    def tearDownClass(cls):
        """Close the database connection after all tests."""
        cls.connection.close()

if __name__ == "__main__":
    unittest.main()
