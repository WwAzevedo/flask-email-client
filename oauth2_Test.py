import base64

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, render_template, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
import jwt


import oauth2


app = Flask(__name__)
app.secret_key = "random secrect"
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="262035376851-7bg725saa0e7nanqp1ce6ltm808bttnm.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'https://www.googleapis.com/auth/gmail.modify openid email profile'},
)


usernames = ['Josias', 'Wesley'] # Triggers

def send_email(username):


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = request.form["Title"].format(usernam)
    msg['From'] = f"{dict(session)['profile']['email']}"
    msg['To'] = request.form['TO']
    msg['Cc'] = None
    send = [msg['To']]

    html = request.form["html"].format(usernam) + str(request.files['file'].read(), 'utf-8')

    # Record the MIME types of both parts - text/plain and text/html.
    html_code = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
    #print("conteudo HTML: "+html_code.as_string())
    # the HTML message, is best and preferred.
    msg.attach(html_code)

    # Send the message via local SMTP server.
    # auth_string = f"user={dict(session)['profile']['email']}\1auth=Bearer {dict(session)['gmail_auth']['access_token']}\1\1"
    # print("Decode: "+auth_string)
    # auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    # #auth_string = generate_oauth2_string(dict(session)['profile']['email'], dict(session)['gmail_auth']['access_token'], as_base64=True)
    # print("TOKEN: "+auth_string)

    smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_conn.set_debuglevel(True)
    smtp_conn.ehlo('test')
    smtp_conn.starttls()
    smtp_conn.docmd('AUTH', 'XOAUTH2 ' + dict(session)['smtp_auth_token'])
    smtp_conn.sendmail(msg['From'], send, msg.as_string())


@app.route('/', methods=["GET", "POST"])
def home():

    if request.method == "POST":

        for usernam in usernames:
            render_template("email.html"), send_email(usernam)
        return render_template("email.html")

    else:
        return render_template("email.html")

@app.route('/login')
def login():

    """Generates the URL for authorizing access.
    This uses the "OAuth2 for Installed Applications" flow described at
    https://developers.google.com/accounts/docs/OAuth2InstalledApp
    Args:
      client_id: Client ID obtained by registering your app.
      scope: scope for access token, e.g. 'https://mail.google.com'
    Returns:
      A URL that the user should visit in their browser.
    """
    redirect_uri = oauth2.GeneratePermissionUrl("262035376851-ons9qsciea2b70v6d5ghd7jqsb0cu5gq.apps.googleusercontent.com", scope='https://www.googleapis.com/auth/gmail.modify openid email profile')
    print("redirect_uri: "+redirect_uri)
    return redirect(redirect_uri)

@app.route('/authorize')
def authorize():

    #Generate Token
    token =  oauth2.AuthorizeTokens("262035376851-ons9qsciea2b70v6d5ghd7jqsb0cu5gq.apps.googleusercontent.com",
                                    "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",
                                    "4/1AX4XfWi48yoZsF7gWzUnJhq9kZDPZBgHGgJMMadAkjkFjFiDBldq_zA2WqM")
    print(token)
    session['token'] = token
    refresh_token = token.get('refresh_token')
    token = oauth2.RefreshToken("262035376851-ons9qsciea2b70v6d5ghd7jqsb0cu5gq.apps.googleusercontent.com",
                                "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",
                                refresh_token)
    # Get Access Token
    session['token'] = token
    print("Access Token: "+session['token']['access_token'])

    # Get user e-mail
    id_token = token.get('id_token')
    decoded = jwt.decode(id_token, options={"verify_signature": False})  # works in PyJWT >= v2.0
    session['profile'] = decoded
    print("User Email: "+session['profile']['email'])

    smtp_auth_token = oauth2.GenerateOAuth2String(session['profile']['email'], session['token']['access_token'])
    print(smtp_auth_token)

    smtp_conn = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_conn.set_debuglevel(True)
    smtp_conn.ehlo()
    # smtp_conn.starttls()
    # smtp_conn.ehlo()
    smtp_conn.docmd('AUTH', 'XOAUTH2 ' + smtp_auth_token)
    smtp_conn.sendmail('weazevedondel@gmail.com', 'wesley.wazevedo@fco.net.br', 'pastel de queijo')

    session['smtp_auth_token'] = smtp_auth_token
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed


    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
