from src.mail import mail

def main():
    mail.send_notification("Something", "123", "2024-05-14")


if __name__ == "__main__":
    main()
