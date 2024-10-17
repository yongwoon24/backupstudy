import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'yongwoon24@gmail.com'  
    smtp_password = 'tifebcdeiswnhlek' 

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(smtp_user, smtp_password) 

        server.sendmail(smtp_user, to_email, msg.as_string())
        print("이메일이 성공적으로 보내졌습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
    finally:
        server.quit() 

subject = "테스트 이메일"
body = "이것은 테스트 이메일입니다."
to_email = "yongwoon24@naver.com" 

send_email(subject, body, to_email)
