import ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_port = 587
smtp_server = "smtp.gmail.com"

email_sender = "checky.pblD@gmail.com"
email_password = "rnkz hrrw kgqe ixfz"

simple_email = ssl.create_default_context()

def send_email(user, system, status, time):
    system_text = "Classroom  🏫" if system == "class" else "Dormitory 🛏️"
    email_receiver = f"{user.studentID}@kmitl.ac.th"

    body = f"""
    {system_text}
    Attendance Status of {user.name}

    Time: {time}
    Status >> {status}  
    """

    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_receiver
    msg["Subject"] = "🔔 Checky Notification"
    msg.attach(MIMEText(body, "plain"))

    text = msg.as_string()

    # Connect to server
    TIE_SERVER = smtplib.SMTP(smtp_server, smtp_port)
    TIE_SERVER.starttls(context=simple_email)
    TIE_SERVER.login(email_sender, email_password)

    # Send email
    TIE_SERVER.sendmail(email_sender, email_receiver, text)

    # Close connection
    TIE_SERVER.quit()