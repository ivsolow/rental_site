import smtpd
import asyncore


class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        decoded_message = data.decode('utf-8')
        print('Received message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        print('Message content:')
        print(decoded_message)


server = CustomSMTPServer(('smtp-server', 1025), None)

print('SMTP server running on localhost:1025')
asyncore.loop()
