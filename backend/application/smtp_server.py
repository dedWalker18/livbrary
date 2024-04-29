from smtpd import SMTPServer
from asyncore import loop

class CustomSMTPServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f"Received message from: {mailfrom}")
        print(f"Recipients: {rcpttos}")
        print(f"Message length: {len(data)}")
        print(f"Message data:\n{data}\n")
        pass
    
def run_server():
    server = CustomSMTPServer(('127.0.0.1', 1025), None)
    print("SMTP server started on port 1025")
    try:
        loop()
    except KeyboardInterrupt:
        print(" Stopping SMTP server...")
        server.close()

if __name__ == "__main__":
    run_server()