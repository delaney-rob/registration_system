from random import randint
from google.appengine.api import mail

def rNumber():
	randomInt = randint(1111111, 9999999)
	return randomInt

def sendRegMail(userName, email, userid):	
	mail.send_mail(sender="Registration Support <robdelaney007@gmail.com>",
              to=userName+" <"+email+">",
              subject="Please confirm your account!!",
              body="""
Dear """+userName+""":

Please confirm your account by visiting the link:

http://empirical-mote-865.appspot.com/verify?type="""+userid+"""

Please let us know if you have any questions.

The Registration Team
""")
	return

def sendResetMail(userName, randomNumber, email):
	rNum = str(randomNumber)
	mail.send_mail(sender="Registration Support <robdelaney007@gmail.com>",
              to=userName+" <"+email+">",
              subject="PASSWORD RESET EMAIL",
              body="""
Dear """+userName+""":

Please reset your password by visiting the link:

http://empirical-mote-865.appspot.com/pwdReset

and enter the information requested including the following code:

"""+rNum+"""

Please let us know if you have any questions.

The Registration Team
""")
	return