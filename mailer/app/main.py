from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

# Database Configuration
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


@app.route("/", methods=["GET", "POST"])
def index():
    config = getSqlConfiguration('../DB/dbconfig.txt')
    conn = create_db_connection(config.get("HOST"), config.get('USER'), config.get('PASSWORD'), config.get('DATABASE'))
    if not conn:
        return "<p>DB Connection Failed</p>"
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        if "add_campaign" in request.form:
            # Adding a new campaign
            campaign_name = request.form["campaign_name"]
            campaign_company = request.form["campaign_company"]
            cursor.execute(
                "INSERT INTO Campaigns (campaign_name, campaign_company, date_created) VALUES (%s, %s, %s)",
                (campaign_name, campaign_company, datetime.now().date())
            )
            conn.commit()
        elif "delete_campaigns" in request.form:
            # Deleting selected campaigns
            selected_campaigns = request.form.getlist("campaign_ids")
            for campaign_id in selected_campaigns:
                print(f"Deleted Campaign with ID {campaign_id}")
                cursor.execute("DELETE FROM Campaigns WHERE campaign_id = %s", (campaign_id,))
            conn.commit()

    # Fetch all campaigns
    cursor.execute("SELECT * FROM Campaigns")
    campaigns = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("campaigns.html", campaigns=campaigns)

if __name__ == "__main__":
    app.run(debug=True)

