from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, render_template, redirect
import os
from Google import Create_Service
import base64

app = Flask(__name__)

usernames = ['Wesley'] # Triggers

# Send e-mail with GMAIL API
def send_email(username, service):

    # Get email to send from page request
    TO = request.form["TO"]

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = request.form["Title"].format(username)
    msg['To'] = request.form["TO"]
    send = [TO]

    # Get HTML from page request
    html = request.form["html"].format(username)       # + str(request.files['file'].read(), 'utf-8')

    # Record the MIME types with html format
    html_code = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    msg.attach(html_code)

    # Record MSG message in an RFC 2822 formatted and base64url encoded string
    raw_string = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    return service.users().messages().send(userId='me', body={'raw': raw_string}).execute()

# Get user e-mail from GMAIL API
def get_user_email(service):
    get_user_email = service.users().getProfile(userId='me').execute()
    user_email = get_user_email['emailAddress''']
    return user_email

# Auth GMAIL API with OAUTH2
def oauth2_gmail_login():
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.readonly']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    return service

# Home route
@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        html = request.form["html"]
        print(html)
        for username in usernames:
            send_email(username, service=oauth2_gmail_login())
        return render_template("email.html")
    elif request.method == "GET":
        return render_template("email.html", user_email=get_user_email(service=oauth2_gmail_login()))

#Login route
@app.route('/login', methods=["GET"])
def login():
    if request.method == "GET":
        oauth2_gmail_login()
        return redirect('http://127.0.0.1:5000/')

if __name__ == '__main__':
    app.run(debug=True)
