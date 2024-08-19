import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('wassimhaimoudi1@gmail.com', '24142424@Yassin')
    print("Connected successfully!")
    server.quit()
except Exception as e:
    print(f"Failed to connect: {e}")
