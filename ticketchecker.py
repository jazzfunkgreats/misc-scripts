#!/usr/bin/python3

import bs4, sys, requests, smtplib

site = 'https://www.residentadvisor.net/event.aspx?902158'
res = requests.get(site)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "lxml")

boxElem = soup.select('#"ticket-Final release"')
if boxElem == []:
    print ("Could not find ticket")
    sys.exit()
else:
    ticketStatus = boxElem[0].get('class')

if ticketStatus[0] != 'closed':
    sender = 'sendmailaddress'
    receiver = 'receivemailaddress'
    headers = """From: %s
To: %s
Subject: Ticket alert!
""" % (sender, receiver)

    message = headers + "\n" + """
Go to RA now you plum! %s
""" % (site)
    try:
        smtpObj = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login('email','pass')
        smtpObj.sendmail(sender, receiver, message)
        smtpObj.quit()
        print ("Successfully sent message")
    except SMTPException:
        print ("Unable to send mail")
else:
    print("Tickets are still closed!")

