import database as db

campaign_number = "1"

menu = """
Select Campaign
Add Campaign
Delete Campaign
Show Targets
Add Targets from CSV
Add Target
Delete Target(s)
Show Senders
Add Senders from CSV
Add Sender
Delete Sender(S)
Show Mail Servers
Add Mail Server
Delete Mail Server
Show Sent Emails
Send Emails by Campaign
Delete Sent Email(s)
Show Recived Requests
Delete Recived Request(s)
Quit
"""


config = db.getSqlConfiguration("dbconfig.txt")
CONN = db.create_db_connection(config["HOST"], config["USER"], config["PASSWORD"], config["DATABASE"])


def select_campaign():
    global campaign_number
    db.displayTable(CONN, 'Campagins')
    choice = input("Enter campaign ID: ")

    query = "SELECT campaign_id, COUNT(*) FROM Campaigns WHERE campaign_id = %s"
    row_count = db.execute_query(CONN, query, choice).rowcount()
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
    db.displayTable(CONN, 'Campagins')
    campaign_choice = input("Enter campaign ID: ")
    db.deleteCampaignById(CONN, campaign_choice)
    return


def show_targets():
    db.displayTable(CONN, 'Targets')
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
    choices = input("Enter the id or range of ids ex. '1-10'")
    start, end = int(choices.split('-')[0]), int(choices.split('-')[1])
    if start and end:
        for i in range(start, end+1):
            db.deleteTargetById(CONN, i)
    else:
        db.deleteTargetById(CONN, choices)
    return


while True:
    current_campaign = db.getCampaignInfo(CONN, campaign_number)
    print(f"Your current campaign is {current_campaign[0]} for {current_campaign[1]} with ID: {current_campaign}")
    print("_"*40)
    print(menu)
    menu_choice = input("Select operation: ")

