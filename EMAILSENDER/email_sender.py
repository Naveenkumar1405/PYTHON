import smtplib
import schedule
import time
import traceback

def send_email():
    email_sender = 'navinmano1412@gmail.com'
    email_password = 'naadtcvzyppgtrzm'
    email_receiver = 'navin@onwords.in'

    subject = 'Scheduled Email'
    body = 'Good Evening, This is a scheduled email sent by Python.'

    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
        traceback.print_exc()

def schedule_email_send():
    schedule.every(1).day.do(send_email)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_email_send()
