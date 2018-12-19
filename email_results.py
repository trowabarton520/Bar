import smtplib


def results_email(text):
    to = ['ben.b.bush@gmail.com', 'trowabarton520@gmail.com', 'Kristi.M.Bush@gmail.com']
    subject = 'Important - 2018 Bar Results'

    gmail_sender = '2018.bar.alert@gmail.com'
    gmail_passwd = 'DidIpass?'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(gmail_sender, gmail_passwd)

    for email in to:
        body = '\r\n'.join(['To: %S'.replace('%S', email),
                            'From: %S'.replace('%S', gmail_sender),
                            'Subject: %S'.replace('%S', subject),
                            'X-Priority: 1',
                            '', text])
        try:
            server.sendmail(gmail_sender, [email], body)
            print('Email Sent')
        except:
            print('Error sending email to ' + email)

    server.quit()


if __name__ == "__main__":
    results_email('Sample Text')
