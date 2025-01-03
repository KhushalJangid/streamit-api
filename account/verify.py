from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import json
def send_otp(email,otp,name):
    import smtplib

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()
    s.ehlo()
    s.login("lumirooms.help@gmail.com", "lumirooms@123")

    msg = MIMEMultipart()

    msg['From']="ZED Corporation"
    msg['To']=email
    msg['Subject']="OTP for Verification"

    msg.attach(MIMEText(f"Hi {name},\nPlease use the OTP below to verify.It is only Valid for 3 minutes.\n\n{otp}\n\n\nPlease don't share your OTP with anyone.\nPlease ignore if you didn't asked for verification.", 'plain'))

    s.send_message(msg)

    s.quit()

def get_otp():
    import pyotp
    secret=pyotp.random_base32()
    otp = pyotp.TOTP(secret)
    return otp.now()
