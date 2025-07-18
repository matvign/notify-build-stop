from src.mail import mail
from src.queries import orders

def main():
    # mail.send_notification("Something", "123", "2024-05-14")
    orders.query()


if __name__ == "__main__":
    main()
