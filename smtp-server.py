import smtpd
import asyncore

# SMTP_SERVER_HOST = 'smtp-server'
SMTP_SERVER_HOST = 'localhost'


class CustomSMTPServer(smtpd.SMTPServer):
    """Тестовый SMTP-сервер для приема
     писем и вывода их содержимого в терминал"""
    def process_message(self, peer, mailfrom,
                        rcpttos,
                        data,
                        **kwargs) -> None:
        decoded_message = data.decode('utf-8')
        print('Received message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        print('Message content:')
        print(decoded_message)


server = CustomSMTPServer((SMTP_SERVER_HOST, 1025), None)

print('SMTP server running on localhost:1025')
asyncore.loop()
