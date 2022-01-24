import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class EmailSender():

    def __init__(self,sender_email,sender_password) -> None:
        
        self.sender = sender_email
        
        self.passw = sender_password
        
        self.msg = MIMEMultipart()

    
    def session_login(self) -> None:
        
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        
        self.server.starttls() # For security
        
        self.server.login(self.sender, self.passw)



    def sendEmail(self,to,subject,text,attachments = []):
        
        self.msg['From'] = self.sender
        
        self.msg['To'] = to
        
        self.msg['Subject'] = subject
        
        self.msg.attach(MIMEText(text, 'plain'))

        if attachments:
            
            for attachment in attachments:
                
                filename = attachment
                
                attachment = open(filename, "rb")

                part = MIMEBase('application', 'octet-stream')
                
                part.set_payload((attachment).read())
                
                encoders.encode_base64(part)
                
                part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                self.msg.attach(part)
        
        self.server.sendmail(self.sender, to, self.msg.as_string())
        
        self.msg = MIMEMultipart()
        
        print(f"Email sent to {to}")


    def killSession(self):
        
        self.server.quit()

