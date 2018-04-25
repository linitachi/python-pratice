
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


def attachcomponent(msg,fileToSend,filetype):
    part = MIMEBase('application',filetype)  #根據檔案型式置換
    part.set_payload( open(fileToSend,"rb").read() )
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment',filename=('UTF-8','',fileToSend)) #NON-ASCII CODE要用UTF-8
    msg.attach(part)

# --- Email 的收件人與寄件人address ---
emailfrom = "testingwaho@gmail.com" 
emailto = "linitachi@gmail.com"
# # --- Email 附件檔案 Attachment ----------- 
fileToSend = "index.csv" 
username = "testingwaho@gmail.com" # --- 寄信的SMTP的帳號---- 
password = "1234@56789a" # --- 寄信的SMTP的密碼---- 

msg = MIMEMultipart() 
msg["From"] = emailfrom 
msg["To"] = emailto 
# --- Email 的主旨 Subject ---
msg["Subject"] = "" 
msg["preamble"] = 'You will not see this in a MIME-aware mail reader.\n' 

#----- Email 的信件內容 Message ----- 
part = MIMEText(u"body text including an Euro char \u20ac\n 中文測試\n ", _charset="UTF-8") 

msg.attach(part) 
#----- Test for Text Message ----- 

attachcomponent(msg,fileToSend,'csv')

# --- 寄件的 SMTP mail server --- 
server = smtplib.SMTP('smtp.gmail.com', 587) 
server.ehlo()
server.starttls()
# --- 如果SMTP server 不需要登入則可把 server.login 用 # mark 掉
server.login(username,password)
server.sendmail(emailfrom, [emailto], msg.as_string())
server.quit()

print('send')