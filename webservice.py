import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, render_template

app = Flask(__name__)


def send_email():
    FROM = request.form["CC"]

    TO = request.form["TO"]
    password = ""

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = request.form["Title"]
    msg['From'] = request.form["CC"]
    msg['To'] = request.form["TO"]

    send = [TO]
    html = request.form["html"] + str(request.files['file'].read(), 'utf-8')

    # Record the MIME types of both parts - text/plain and text/html.
    html_code = MIMEText(html.encode('utf-8'), 'html', 'utf-8')

    # Attach parts into message container.
    # the HTML message, is best and preferred.
    msg.attach(html_code)

    # Send the message via local SMTP server.

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(FROM, password)
    server.sendmail(FROM, send, msg.as_string())


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        TO = request.form["TO"]
        CC = request.form["CC"]
        Title = request.form["Title"]
        html = request.form["html"]
        print(TO, CC, Title, html)
        return render_template("email.html"), send_email()
    else:
        return render_template("email.html")


if __name__ == '__main__':
    app.run(debug=True)
