from flask import Flask, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # Replace with your MySQL username
        password="Gova@12345",  # Replace with your MySQL password
        database="offer_db"     # Replace with your MySQL database name
    )

# USSD route
@app.route('/ussd', methods=['POST'])
def ussd():
    ussd_input = request.form.get('text')  # Get input from the USSD query
    offer_codes = ussd_input.split('*')[1:]  # Extract offer codes

    # Connect to MySQL database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Prepare the response
    response = ""
    
    for offer_code in offer_codes:
        cursor.execute("SELECT * FROM offers WHERE offer_code = %s", (offer_code.strip(),))
        offer = cursor.fetchone()

        if offer:
            # Check if the offer is valid and not expired
            expiration_date = offer['expiration_date']  # No need to call .date()
            if offer['is_valid'] == 1 and expiration_date > datetime.today().date():
                response += f"CODE {offer_code}: {offer['discount']}% off at {offer['company']}.\n"
            else:
                response += f"CODE {offer_code}: Invalid or Expired Offer.\n"
        else:
            response += f"CODE {offer_code}: Offer not found.\n"

    cursor.close()
    conn.close()

    return response

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
