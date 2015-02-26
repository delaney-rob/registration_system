
#   10% of final grade.
#   Due Wed. 4th March 2015 - end of the day.
#   All code in Python, GAE, and webapp2.
#   Deploy on GAE.

import os
import re
import webapp2
import jinja2
from gaesessions import get_current_session
from google.appengine.ext import ndb
from google.appengine.ext import db
from utilities import rNumber, sendRegMail, sendResetMail

class pendUserDetail(ndb.Model):
    userid = ndb.StringProperty()
    userName = ndb.StringProperty()
    email = ndb.StringProperty()
    passwd = ndb.StringProperty()     
    ranNumber = ndb.IntegerProperty()

class cfirmUserDetail(ndb.Model):
    userid = ndb.StringProperty()
    email = ndb.StringProperty()
    passwd = ndb.StringProperty()    
    userName = ndb.StringProperty()
    ranNumber = ndb.IntegerProperty() 
    emailCodeUsed = ndb.StringProperty()

JINJA = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)

class LoginHandler(webapp2.RequestHandler):
    def get(self):  
        session = get_current_session()      
        template = JINJA.get_template('login.html')
        self.response.write(template.render(
            { 'the_title': 'Welcome to the Login Page' ,
              'noDisplayLinks': 'noDisplayLinks',
              'action': '/processlogin'} 
        ))       

    def post(self):
        session = get_current_session()
        session['userid'] = self.request.get('userid')         
        session['passwd'] = self.request.get('passwd')
        errorList = []
        if len(session['userid']) < 4  :
            errorList.append('User ID is too short or has not been entered.')
        if len(session['passwd']) < 4 :
            errorList.append('Password is too short or has not been entered.')

        if errorList != []:
            template = JINJA.get_template('login.html')
            self.response.write(template.render(
            { 'the_title': 'Welcome to the Login Page' ,
              'noDisplayLinks': 'noDisplayLinks',
              'errors': errorList,
              'action': '/login'} 
            ))
        else:
            # Lookup login ID in "confirmed" datastore.
            query = ndb.gql("SELECT * FROM cfirmUserDetail WHERE userid = :1", session['userid'])
            ret = query.fetch()        
            if ret == []:
                session.clear()
                errorList.append('The user ID you have entered does not exist.')
                template = JINJA.get_template('login.html')
                self.response.write(template.render(
                { 'the_title': 'Welcome to the Login Page' ,
                  'errors': errorList,
                  'noDisplayLinks': 'noDisplayLinks',
                  'action': '/processlogin'} 
                ))
            else:                
                for x in ret:
                    # Check for password match.
                    if session['userid'] == x.userid and session['passwd'] == x.passwd:
                        print("All ok")
                        template = JINJA.get_template('login.html')
                        self.response.write(template.render(
                        { 'the_title': 'Welcome to the Login Page' ,
                          'verifydets': 'You are now logged in.',
                          'displayLinks': 'displayLinks',
                          'action': '/processlogin'} 
                        ))
                    else:                        
                        session.clear()
                        errorList = ['The password you supplied is incorrect.']
                        template = JINJA.get_template('login.html')
                        self.response.write(template.render(
                        { 'the_title': 'Welcome to the Login Page' ,
                          'noDisplayLinks': 'noDisplayLinks',
                          'errors': errorList,
                          'action': '/processlogin'}
                        ))  
        
    # Check that a login and password arrived from the FORM.
    # What if the user has forgotten their password?  Provide a password-reset facility/form.
    
# We need to provide for LOGOUT.

class Page1Handler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        errors=[]
        if session.get('userid') != None:            
            template = JINJA.get_template('page1.html')
            self.response.write(template.render(
            { 'the_title': 'Welcome to the Page 1' ,              
              'displayLinks': 'displayLinks',
              'action': '/processlogin'} 
            ))

        else:
            session.clear()
            errors.append('You cannot view Page 1 as you are not logged in.')
            template = JINJA.get_template('login.html')
            self.response.write(template.render(
            { 'the_title': 'Welcome to the Login Page' ,
              'noDisplayLinks': 'noDisplayLinks',
              'errors': errors,
              'action': '/login'}
            ))

class Page2Handler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        errors=[]        
        if session.get('userid') != None:            
            template = JINJA.get_template('page2.html')
            self.response.write(template.render(
            { 'the_title': 'Welcome to the Page 2' ,              
              'displayLinks': 'displayLinks',
              'action': '/processlogin'} 
            ))

        else:
            session.clear()
            errors.append('You cannot view Page 2 as you are not logged in.')
            template = JINJA.get_template('login.html')
            self.response.write(template.render(
            { 'the_title': 'Welcome to the Login Page' ,
              'noDisplayLinks': 'noDisplayLinks',
              'errors': errors,
              'action': '/login'}
            ))            

class Page3Handler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        errors=[]        
        if session.get('userid') != None:            
            template = JINJA.get_template('page3.html')
            self.response.write(template.render(
            { 'the_title': 'Welcome to the Page 3' ,              
              'displayLinks': 'displayLinks',
              'action': '/processlogin'} 
            ))

        else:
            session.clear()
            errors.append('You cannot view Page 3 as you are not logged in.')
            template = JINJA.get_template('login.html')
            self.response.write(template.render(
            { 'the_title': 'Welcome to the Login Page' ,
              'noDisplayLinks': 'noDisplayLinks',
              'errors': errors,
              'action': '/login'}
            ))

class RegisterHandler(webapp2.RequestHandler):
    def get(self):        
        template = JINJA.get_template('reg.html')
        self.response.write(template.render(
            { 'the_title': 'Welcome to the Registration Page' ,
              'noDisplayLinks': 'noDisplayLinks',
              'action': '/processreg'} 
        ))

    def post(self):
        session = get_current_session()
        session['userid'] = self.request.get('userid')
        session['email'] = self.request.get('email') 
        session['passwd'] = self.request.get('passwd')
        session['userName'] = self.request.get('username')
        password = self.request.get('passwd')
        passwd2 = self.request.get('passwd2')        

        # Check if the data items from the POST are empty.
        errorList=[]        
        if len(session['userid']) < 5 :
            errorList.append('User ID must be greater than five characters in length.')
        if len(session['email']) < 5:
            errorList.append('Email must be a minimum length of five characters.')
        # Is the password too simple?
        if len(session['passwd']) > 8 or len(session['passwd']) < 4:        
            errorList.append('Password must be between 4 and 8 characters long.')         
        #if re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])$', password) is not None:
        if re.match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])', password) is None:
            errorList.append('Password must contain at least one lower case character, one upper case character and one number')         
        if session['passwd'] != passwd2:
            errorList.append('Passwords do not match.')        
        if errorList != []:
            session.clear()
            template = JINJA.get_template('reg.html')
            self.response.write(template.render(
                { 'the_title': 'Welcome to the Registration Page',
                  'action': '/register',
                  'noDisplayLinks': 'noDisplayLinks',
                  'errors': errorList }            
            ))
        else:
            # Does the userid already exist in the "confirmed" datastore or in "pending"?            
            query = ndb.gql("SELECT * FROM pendUserDetail WHERE userid = :1", session['userid'])
            ret = query.fetch()
            if ret == []: 
                # Add registration details to "pending" datastore.               
                person = pendUserDetail()
                person.userid = session['userid']
                person.email = session['email']
                person.passwd = session['passwd']                
                ranNumber = str(rNumber())                
                person.ranNumber = int(ranNumber)
                person.userName = session['userName']
                person.put() 
                # Send confirmation email.
                sendRegMail(session['userName'], session['email'], session['userid'])
                template = JINJA.get_template('login.html')
                self.response.write(template.render(
                    { 'the_title': 'Welcome to the login page',
                    'action': '/login',
                    'noDisplayLinks': 'noDisplayLinks',
                    'verifydets': "Please check your email to verify your new account.",
                    'errors': errorList }   
                ))
            else:
                session.clear()
                errorList.append('That user name is already in use, please choose another.')
                template = JINJA.get_template('reg.html')
                self.response.write(template.render(
                    { 'the_title': 'Registration',
                    'action': '/register',
                    'noDisplayLinks': 'noDisplayLinks',
                    'errors': errorList }            
            )) 

class Verificationhandler(webapp2.RequestHandler):
    def get(self): 
        userType = self.request.get('type') 
        query = ndb.gql("SELECT * FROM pendUserDetail WHERE userid = :1", userType)  
        ret = query.fetch()
        cPerson = cfirmUserDetail()
        for i in ret:
            cPerson.userid = i.userid
            cPerson.passwd = i.passwd
            cPerson.email = i.email
            cPerson.userName = i.userName
            cPerson.ranNumber = i.ranNumber
            cPerson.emailCodeUsed = "Yes"
            cPerson.put() 
        template = JINJA.get_template('login.html')
        if userType == "":
            self.response.write(template.render(
                { 'the_title': 'Welcome to the login page' ,                  
                  'noDisplayLinks': 'noDisplayLinks',
                  'action': '/processlogin'} 
            ))
        else:
            self.response.write(template.render(
                { 'the_title': 'Welcome to the login page' ,
                  'verifydets': "Account has been verified, please log in!",
                  'noDisplayLinks': 'noDisplayLinks',
                  'action': '/processlogin'} 
            ))

    def post(self):
        pass

class LogoutHandler(webapp2.RequestHandler):
    def get(self): 
        session = get_current_session()
        session.clear()
        self.redirect('/')

class PasswordHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA.get_template('pwdReset.html')
        self.response.write(template.render(
            { 'the_title': 'Password Reset Page' , 
              'noDisplayLinks': 'noDisplayLinks',             
              'action': '/pwdReset'} 
        ))

    def post(self):
        resetType = self.request.get('resetType')
        if resetType =='enterCode':
            template = JINJA.get_template('pwdCodeEnter.html')
            self.response.write(template.render(
                { 'the_title': 'Password Reset Code Entry' ,
                  'noDisplayLinks': 'noDisplayLinks',              
                  'action': '/resetPassword'} 
            ))            
        elif resetType =='sendCode':
            template = JINJA.get_template('pwdCodeRequest.html')
            self.response.write(template.render(
                { 'the_title': 'Password Reset Code Request' , 
                  'noDisplayLinks': 'noDisplayLinks',             
                  'action': '/pwdProcessing'} 
            ))
        else:
            print("Code type unknown: " + resetType)

class PasswordProcessHandler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        session.clear()
        self.redirect('/pwdReset')        
    def post(self):
        userID = self.request.get('userid') 
        userEmail = self.request.get('email')
        query = ndb.gql("SELECT * FROM cfirmUserDetail WHERE userid = :1", userID)  
        ret = query.fetch()
        if ret == []:
            errorList=['User ID does not exist']
            template = JINJA.get_template('pwdCodeRequest.html')
            self.response.write(template.render(
                { 'the_title': 'Password Reset Code Request' ,
                  'noDisplayLinks': 'noDisplayLinks',              
                  'action': '/pwdProcessing',
                  'errors': errorList} 
            ))
        else:
            for x in ret:
                if userID == x.userid and userEmail != x.email:
                    errorList=['The email address you supplied does not match email address on file']
                    template = JINJA.get_template('pwdCodeRequest.html')
                    self.response.write(template.render(
                        { 'the_title': 'Password Reset Code Request' ,              
                          'action': '/pwdProcessing',
                          'noDisplayLinks': 'noDisplayLinks',
                          'errors': errorList} 
                    ))
                else:
                    newRanCode = rNumber()
                    x.ranNumber = newRanCode
                    x.emailCodeUsed = "No"
                    x.put()
                    sendResetMail(x.userName, newRanCode, x.email)
                    template = JINJA.get_template('login.html')
                    self.response.write(template.render(
                        { 'the_title': 'Welcome to the login page' ,              
                          'action': '/login',
                          'noDisplayLinks': 'noDisplayLinks',
                          'verifydets': 'Please check your email for password reset instructions'} 
                    ))

class ResetPasswordHandler(webapp2.RequestHandler):
    def get(self):        
        self.redirect('/pwdReset')
    def post(self):
        userID = self.request.get('userid')
        userEmail = self.request.get('email')
        userEmailCode = self.request.get('resetCode')
        userPwd = self.request.get('passwd')
        userPwd2 = self.request.get('passwd2')

        query = ndb.gql("SELECT * FROM cfirmUserDetail WHERE userid = :1", userID)  
        ret = query.fetch()
        errorList = []
        if ret == []:
            errorList.append('User ID supplied is not registered on this system.')            

        for x in  ret:            
            if userEmail != x.email:
                errorList.append('Email supplied does not match with email recorded against user ID on system.')
            elif str(userEmailCode) != str(x.ranNumber):
                errorList.append('Password reset code does not match the one supplied by email.')
            elif x.emailCodeUsed == "Yes":
                errorList.append('Password has already been reset using this password reset code, please request another.')
        
        if len(userID) < 5 :
            errorList.append('User ID must be greater than five characters in length.')
        if len(userEmail) < 5:
            errorList.append('Email must be a minimum length of five characters.')
        # Is the password too simple?
        if len(userPwd) > 8 or len(userPwd) < 4:        
            errorList.append('Password must be between four and eight characters long.')         
        #if re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])$', password) == None:
        #    errorList.append('Password must contain at least one lower case character, one upper case character and one number')  
        #    print(password) 
        #Check if passwd == passwd2.
        if userPwd != userPwd2:
            errorList.append('Passwords do not match.')

        if errorList != []:
            template = JINJA.get_template('pwdCodeEnter.html')
            self.response.write(template.render(
                { 'the_title': 'Password Reset Code Entry',
                  'noDisplayLinks': 'noDisplayLinks',
                  'action': '/resetPassword',
                  'errors': errorList }            
            ))

        else:
            for x in ret:
                x.passwd = userPwd
                x.emailCodeUsed = "Yes"
                x.put()
            template = JINJA.get_template('login.html')
            self.response.write(template.render(
                { 'the_title': 'Welcome to the login page' ,
                  'verifydets': "Password has been reset, please log in!",
                  'noDisplayLinks': 'noDisplayLinks',
                  'action': '/login'} 
            ))

app = webapp2.WSGIApplication([
    ('/register', RegisterHandler),
    ('/processreg', RegisterHandler),
    ('/verify', Verificationhandler),
    ('/processverify', Verificationhandler),
    ('/', LoginHandler),
    ('/login', LoginHandler),
    ('/processlogin', LoginHandler),
    ('/logout', LogoutHandler),
    ('/pwdReset', PasswordHandler),
    ('/pwdProcessing', PasswordProcessHandler),
    ('/resetPassword', ResetPasswordHandler),
    # Next three URLs are only available to logged-in users.
    ('/page1', Page1Handler),
    ('/page2', Page2Handler),
    ('/page3', Page3Handler),
], debug=True)