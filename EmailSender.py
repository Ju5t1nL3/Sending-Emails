"""
Email sender that can allow you to add a subject and message, as well as 
choose whom you would like to send, cc, and bcc the email to.
"""

from email.message import EmailMessage
from Secret import my_password
import ssl
import smtplib

def email_list(temp):
    """
    Returns a string that contains emails separated by commas and no spaces (can store a singular email).
    Asks different questions depending on TEMP. It must return at least one email.
    """
    accepted = ["y", "yes", "n", "no"]
    accepted_yes = ["y", "yes"]

    nextStep = False
    nextStep2 = False
    nextStep3 = False
    email_whom = ""

    while nextStep == False:
        nextStep2 = False
        nextStep3 = False
        while nextStep2 == False:
            to_temp = input(f"Who would you like to {temp} this email to?").strip()
            if to_temp.isspace() or to_temp == "":
                print("An email is required.")
            else:
                nextStep2 = True
                email_whom += to_temp
        while nextStep3 == False:
            answer = input (f"Would you like to {temp} this email to anyone else (Y/N)?").lower().strip()
            if answer in accepted:
                nextStep3 = True
                if answer in accepted_yes:
                    email_whom += ","
                else:
                    nextStep = True
            else:
                print("Please give an appropriate answer.")
    
    return email_whom

def continue_on(temp):
    """
    Returns a string that contains emails separated by commas and no spaces (can store a singular email).
    Asks different questions depending on TEMP. However, is different from email_list in that it CAN
    return empty strings. In other words, this list does NOT need to be filled with emails.
    """
    accepted = ["y", "yes", "n", "no"]
    accepted_yes = ["y", "yes"]

    nextStep = False

    while nextStep == False:
        answer = input(f"Would you like to {temp} this email to anyone (Y/N)?").lower().strip()
        if answer in accepted:
            nextStep = True
            if answer in accepted_yes:
                return email_list(temp)
            else:
                nextStep = True
                return ""
        else:
            print("Please give an appropriate answer.")

email_sender = "justinle2006@gmail.com" #change this to your gmail email if you would like to try
email_password = my_password #this is the password from two factor authentification

#sets email headers
email_to = email_list("send") 
email_cc = continue_on("CC")
email_bcc = continue_on("BCC")

nextStep = False
while nextStep == False:
    subject = input("Please enter a subject.")
    if subject.isspace() or subject == "":
        print("A subject is required for the email.")
    else:
        nextStep = True

#sets message of email
body = input("Please enter a message.")

msg = EmailMessage()
msg['From'] = email_sender
msg['To'] = email_to
msg['subject'] = subject
msg['CC'] = email_cc
msg.set_content(body)

recipients = email_to.split() + email_cc.split(",") + email_bcc.split(",")

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, recipients, msg.as_string())