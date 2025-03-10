import database as db

config = db.getSqlConfiguration("dbconfig.txt")

conn = db.create_db_connection(config["HOST"], config["USER"], config["PASSWORD"], config["DATABASE"])

#db.deleteCampaignById(conn, 1)

db.createTables(conn)

#db.addCampaign(conn, 'test', 'test_company')

#db.addSender(conn, 'first', 'last', 'fromemail@mail.com', 'mailfrom@mail.com', 'senderPosition', 'senderDepartment', 'test', 1, 'test_compnay')

#db.addEmailServer(conn, 'oracle', '../../mailconfig.txt')

db.addTarget(conn, 'first', 'last', 'targetEmail@mail.com', 'Position', 'department', 1)

db.sendEmailByCampaign(conn, 1, 1, 1, "test email")
