import database as db
import re

campaign_number = ""

menu = """
1. Select Campaign
2. Add Campaign
3. Delete Campaign
4. Show Targets
5. Add Targets from CSV
6. Add Target
7. Delete Target(s)
8. Show Senders
9. Add Senders from CSV
10. Add Sender
11. Delete Sender(S)
12. Show Mail Servers
13. Add Mail Server
14. Delete Mail Server
15. Show Sent Emails
16. Send Emails by Campaign
17. Delete Sent Email(s)
18. Show Recived Requests
19. Delete Recived Request(s)
20. Quit
"""


config = db.getSqlConfiguration("dbconfig.txt")
CONN = db.create_db_connection(config["HOST"], config["USER"], config["PASSWORD"], config["DATABASE"])


def select_campaign():
    global campaign_number
    db.displayTable(CONN, 'Campaigns')
    choice = input("Enter campaign ID: ")

    query = "SELECT COUNT(*) FROM Campaigns WHERE campaign_id = %s"
    row_count = db.execute_query(CONN, query, (choice,)).fetchone()
    row_count = row_count[0]
    if row_count > 0:
        campaign_number = choice
    else:
        print(f"Could not find a campaign with ID {choice}.")
    return


def add_campaign():
    campaign_name = input("Enter campaign name: ")
    campaign_company = input("Enter campaign company: ")
    db.addCampaign(CONN, campaign_name, campaign_company)
    return


def delete_campaign():
    db.displayTable(CONN, 'Campaigns')
    campaign_choice = input("Enter campaign ID: ")
    if campaign_choice == campaign_number:
        print("Can not delete active Campaign.")
        return
    print(f"{'#'*100}\nWarning! Deleting a campaign will delte all data related to the campaign do you want to proceede.{'#'*100}")
    choice = input(f'Enter \"I want to delete all data for {campaign_choice}\".')
    if choice == f"I want to delete all data for {campaign_choice}":
        db.deleteCampaignById(CONN, campaign_choice)
    else:
        print("Camapign was not deleted.")
    return


def show_targets():
    db.displayTableByCampaign(CONN, 'Targets', campaign_number)
    return


def add_targets_csv():
    csv_location = input("Enter path to CSV file: ")
    db.addTargetsCSV(CONN, csv_location, campaign_number)
    return


def add_target():
    target_first = input("Enter target's first name: ")
    target_last = input("Enter target's last name: ")
    target_email = input("Enter target's email: ")
    target_position = input("Enter target's position: ")
    target_department = input("Enter target's department: ")
    db.addTarget(CONN, target_first, target_last, target_email, target_position, target_department, campaign_number)
    return


def delete_targets():
    show_targets()
    start = 0
    end = 0
    choices = input("Enter the id or range of ids ex. '1-10'")
    try:
        start, end = int(choices.split('-')[0]), int(choices.split('-')[1])
    except IndexError:
        start = int(choices)
    if start and end:
        for i in range(start, end+1):
            db.deleteTargetById(CONN, i)
    else:
        db.deleteTargetById(CONN, choices)
    return


def show_senders():
    db.displayTableByCampaign(CONN, 'Senders', campaign_number)
    return


def add_senders_csv():
    csv_location = input("Enter path to CSV file: ")
    db.addSendersCSV(CONN, csv_location, campaign_number)
    return


def add_sender():
    sender_first = input("Enter senders's first name: ")
    sender_last = input("Enter senders's last name: ")
    email_from = input("Enter senders's from email: ")
    email_mail_from = input("Enter sender's mail from email: ")
    sender_position = input("Enter target's position: ")
    sender_department = input("Enter target's department: ")
    db.addTarget(CONN, sender_first, sender_last, email_mail_from, email_from, sender_position, sender_department, campaign_number)
    return


def delete_senders():
    show_senders()
    start = 0
    end = 0
    choices = input("Enter the id or range of ids ex. '1-10'")
    try:
        start, end = int(choices.split('-')[0]), int(choices.split('-')[1])
    except IndexError:
        start = int(choices)
    if start and end:
        for i in range(start, end+1):
            db.deleteSenderById(CONN, i)
    else:
        db.deleteSenderById(CONN, choices)
    return


def show_mail_servers():
    db.displaytable(CONN, 'Email_Servers')
    return


def add_mail_server():
    location = input("Enter the path to the mail server config: ")
    server_name = input("Enter the name for the mail server: ")
    db.addEmailServer(CONN, server_name, location)
    return


def delete_mail_server():
    choice = input("Enter the ID of the server: ")
    db.deleteServerById(CONN, choice)
    return


def show_sent():
    db.displayTable(CONN, 'Sent_Emails')
    return


def send_emails():
    sender = input("Enter sender ID: ")
    mail_server = input("Enter mail server ID: ")
    subject = input("Enter the subject of the email: ")
    template_location = input("Enter the path of the template: ")
    db.sendEmailByCampaign(CONN, campaign_number, sender, mail_server, subject, template_location)


def delete_sent_emails():
    show_sent()
    start = 0
    end = 0
    choices = input("Enter the id or range of ids ex. '1-10'")
    try:
        start, end = int(choices.split('-')[0]), int(choices.split('-')[1])
    except IndexError:
        start = int(choices)
    if start and end:
        for i in range(start, end+1):
            db.deleteSentEmailById(CONN, i)
    else:
        db.deleteSentEmailById(CONN, choices)
    return


while True:
    if not campaign_number:
        print("No campaign selected please select one before continuing.")
    else:
        current_campaign = db.getCampaignInfo(CONN, campaign_number)
        print(f"Your current campaign is {current_campaign[0]} for {current_campaign[1]} with ID: {campaign_number}")
    print("#"*100)
    print(menu)
    menu_choice = input("Select operation: ")
    if not re.match('1[0-9]|[1-9]', menu_choice):
        print(f"Invalid input {menu_choice}")
        continue
    menu_choice = int(menu_choice)

    if menu_choice == 1:
        select_campaign()
        continue
    elif menu_choice == 2:
        add_campaign()
        continue
    elif menu_choice == 3:
        delete_campaign()
        continue
    elif menu_choice == 4:
        show_targets()
        continue
    elif menu_choice == 5:
        add_targets_csv()
        continue
    elif menu_choice == 6:
        add_target()
        continue
    elif menu_choice == 7:
        delete_targets()
        continue
    elif menu_choice == 8:
        show_senders()
        continue
    elif menu_choice == 9:
        add_senders_csv()
        continue
    elif menu_choice == 10:
        add_sender()
        continue
    elif menu_choice == 11:
        delete_senders()
        continue
    elif menu_choice == 12:
        show_mail_servers()
        continue
    elif menu_choice == 13:
        add_mail_server()
        continue
    elif menu_choice == 14:
        delete_mail_server()
        continue
    elif menu_choice == 15:
        show_sent()
        continue
    elif menu_choice == 16:
        send_emails()
        continue
    elif menu_choice == 17:
        delete_sent_emails()
        continue
    elif menu_choice == 18:
        continue
    elif menu_choice == 19:
        continue
    elif menu_choice == 20:
        quit()
        continue
