import hashlib
import os
import re

import pandas


def hash_password(password):
    """Hash a password using SHA-256 for secure storage and comparison."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_hotels():
    """Load hotel data from CSV."""
    csv_path = os.path.join(os.path.dirname(__file__), "hotels.csv")
    return pandas.read_csv(csv_path, dtype={"id": str})


def load_cards():
    """Load card data from CSV."""
    csv_path = os.path.join(os.path.dirname(__file__), "cards.csv")
    return pandas.read_csv(csv_path, dtype=str).to_dict(orient="records")


def load_card_security():
    """Load card security data from CSV."""
    csv_path = os.path.join(os.path.dirname(__file__), "card_security.csv")
    return pandas.read_csv(csv_path, dtype=str)


class Hotel:

    def __init__(self, hotel_id, df):
        self.hotel_id = hotel_id
        self.df = df
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book a hotel by changing its availability to no"""
        self.df.loc[self.df["id"] == self.hotel_id, "available"] = "no"
        csv_path = os.path.join(os.path.dirname(__file__), "hotels.csv")
        self.df.to_csv(csv_path, index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = self.df.loc[
            self.df["id"] == self.hotel_id, "available"
        ].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {
            "number": self.number,
            "expiration": expiration,
            "holder": holder,
            "cvc": cvc,
        }
        df_cards = load_cards()
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        df_cards_security = load_card_security()
        password_hash = df_cards_security.loc[
            df_cards_security["number"] == self.number, "password"
        ].squeeze()
        if password_hash == hash_password(given_password):
            return True
        else:
            return False


def validate_hotel_id(hotel_id, df):
    """Validate that the hotel_id exists in the dataset."""
    if not hotel_id.strip():
        return False
    return hotel_id in df["id"].values


def sanitize_name(name):
    """Sanitize customer name input to allow only safe characters."""
    name = name.strip()
    if not name:
        return None
    # Allow letters, spaces, hyphens, apostrophes, and periods only
    if not re.match(r"^[a-zA-Z\s\-'.]+$", name):
        return None
    return name


def main():
    df = load_hotels()
    print(df)

    hotel_id = input("Enter the id of the hotel: ")
    if not validate_hotel_id(hotel_id, df):
        print("Invalid hotel ID. Please enter a valid hotel ID from the list.")
        return

    hotel = Hotel(hotel_id, df)

    if hotel.available():
        card_number = input("Enter your credit card number: ")
        card_expiration = input("Enter card expiration (MM/YY): ")
        card_holder = input("Enter card holder name: ")
        card_cvc = input("Enter card CVC: ")

        credit_card = SecureCreditCard(number=card_number)

        if credit_card.validate(
            expiration=card_expiration, holder=card_holder, cvc=card_cvc
        ):
            card_password = input("Enter your credit card password: ")
            if credit_card.authenticate(given_password=card_password):
                name = input("Enter your name: ")
                sanitized_name = sanitize_name(name)
                if sanitized_name is None:
                    print(
                        "Invalid name. Please use only letters, spaces, "
                        "hyphens, apostrophes, and periods."
                    )
                    return
                hotel.book()
                reservation_ticket = ReservationTicket(
                    customer_name=sanitized_name, hotel_object=hotel
                )
                print(reservation_ticket.generate())
            else:
                print("Credit card authentication failed.")
        else:
            print("There was a problem with your payment.")
    else:
        print("Hotel is not free.")


if __name__ == "__main__":
    main()



