def addTarget(connection, targetFirst, targetLast, targetEmail, targetPosition, targetDepartment, campaignName, campaignId, targetCompany):
    query = """
    INSERT INTO Targets (target_first, target_last, target_email, target_position, target_department, campaign_name, campaign_id, target_company, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    values = (targetFirst, targetLast, targetEmail, targetPosition, targetDepartment, campaignName, campaignId, targetCompany)
    execute_query(connection, query, values)


def addSender(connection, senderFirst, senderLast, fromEmail, mailFromEmail, senderPosition,
              senderDepartment, campaignName, campaignId, senderCompany):
    query = """
    INSERT INTO Senders (sender_first, sender_last, from_email, mail_from_email, sender_position, sender_department, campaign_name, campaign_id, sender_company, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    values = (senderFirst, senderLast, fromEmail, mailFromEmail, senderPosition, senderDepartment, campaignName, campaignId, senderCompany)
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
    query = "DELETE FROM Sent_Emails WHERE id = %s"
    execute_query(connection, query, (email_id,))


