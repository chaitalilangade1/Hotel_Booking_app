# Hotel Booking App - Wiki

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
  - [Class Diagram](#class-diagram)
  - [Classes](#classes)
- [Data Files](#data-files)
  - [hotels.csv](#hotelscsv)
  - [cards.csv](#cardscsv)
  - [card_security.csv](#card_securitycsv)
- [Application Flow](#application-flow)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
- [Example Walkthrough](#example-walkthrough)
- [Configuration](#configuration)
- [Contributing](#contributing)

---

## Overview

The **Hotel Booking App** is a command-line Python application that allows users to browse available hotels and make reservations. It features a credit card payment system with two-factor authentication (card validation + password verification) to ensure secure bookings. Upon a successful booking, a reservation ticket is generated for the customer.

---

## Features

- **Hotel Listing**: View all available hotels with details such as name, city, capacity, and availability.
- **Hotel Booking**: Book a hotel by selecting its ID from the listed options.
- **Credit Card Validation**: Validates credit card details (number, expiration date, holder name, and CVC) against stored records.
- **Secure Authentication**: Adds an extra layer of security by requiring a password associated with the credit card.
- **Reservation Ticket Generation**: Generates a confirmation ticket with booking details upon successful reservation.
- **Persistent Data Storage**: Hotel availability is updated in the CSV file after each booking, ensuring data persistence.

---

## Project Structure

```
Hotel_Booking_app/
|-- main.py                # Main application entry point with all classes and logic
|-- hotels.csv             # Hotel data (id, name, city, capacity, availability)
|-- cards.csv              # Credit card data for validation
|-- card_security.csv      # Credit card passwords for authentication
|-- planning.txt           # Project planning notes
|-- .idea/                 # IDE configuration (PyCharm/IntelliJ)
```

---

## Architecture

### Class Diagram

```
+-------------------+
|      Hotel        |
+-------------------+
| - hotel_id: str   |
| - name: str       |
+-------------------+
| + __init__(id)    |
| + book()          |
| + available()     |
+-------------------+

+------------------------+
|   ReservationTicket    |
+------------------------+
| - customer_name: str   |
| - hotel: Hotel         |
+------------------------+
| + __init__(name, hotel)|
| + generate()           |
+------------------------+

+------------------------+
|     CreditCard         |
+------------------------+
| - number: str          |
+------------------------+
| + __init__(number)     |
| + validate(exp, holder,|
|            cvc)        |
+------------------------+
          ^
          | inherits
+------------------------+
|   SecureCreditCard     |
+------------------------+
| + authenticate(pwd)    |
+------------------------+
```

### Classes

#### `Hotel`

Represents a hotel entity. Reads hotel data from `hotels.csv`.

| Method        | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `__init__(hotel_id)` | Initializes the hotel with its ID and retrieves its name from the CSV. |
| `book()`      | Marks the hotel as unavailable (`"no"`) in the CSV file.                    |
| `available()` | Returns `True` if the hotel is available, `False` otherwise.                |

#### `ReservationTicket`

Generates a reservation confirmation for the customer.

| Method                        | Description                                              |
|-------------------------------|----------------------------------------------------------|
| `__init__(customer_name, hotel_object)` | Stores customer name and the associated hotel object. |
| `generate()`                  | Returns a formatted string with the booking confirmation. |

#### `CreditCard`

Handles credit card validation against stored card records.

| Method                                  | Description                                                              |
|-----------------------------------------|--------------------------------------------------------------------------|
| `__init__(number)`                      | Initializes the credit card with its number.                             |
| `validate(expiration, holder, cvc)`     | Checks if card details match any record in `cards.csv`. Returns `True`/`False`. |

#### `SecureCreditCard` (extends `CreditCard`)

Adds password-based authentication on top of credit card validation.

| Method                        | Description                                                                  |
|-------------------------------|------------------------------------------------------------------------------|
| `authenticate(given_password)` | Verifies the given password against the stored password in `card_security.csv`. Returns `True`/`False`. |

---

## Data Files

### `hotels.csv`

Stores hotel information. Each row represents a hotel.

| Column      | Type   | Description                                  |
|-------------|--------|----------------------------------------------|
| `id`        | String | Unique identifier for the hotel              |
| `name`      | String | Name of the hotel                            |
| `city`      | String | City where the hotel is located              |
| `capacity`  | Int    | Maximum number of guests                     |
| `available` | String | Availability status (`"yes"` or `"no"`)      |

**Sample Data:**

| id  | name                     | city        | capacity | available |
|-----|--------------------------|-------------|----------|-----------|
| 134 | Tourist Sunny Apartment  | Anchorage   | 4        | no        |
| 188 | Snow Palace              | New Delhi   | 5        | yes       |
| 655 | City Break Inn           | Porto-Novo  | 3        | no        |

### `cards.csv`

Stores credit card information used for payment validation.

| Column       | Type   | Description                     |
|--------------|--------|---------------------------------|
| `number`     | String | Credit card number              |
| `expiration` | String | Expiration date (MM/YY format)  |
| `cvc`        | String | Card verification code          |
| `holder`     | String | Name of the cardholder          |

### `card_security.csv`

Stores passwords associated with credit cards for two-factor authentication.

| Column     | Type   | Description                          |
|------------|--------|--------------------------------------|
| `number`   | String | Credit card number                   |
| `password` | String | Password for secure authentication   |

---

## Application Flow

The application follows this sequential flow:

```
START
  |
  v
Display list of hotels (from hotels.csv)
  |
  v
User enters a hotel ID
  |
  v
Check hotel availability
  |
  +-- NOT available --> "Hotel is not free." --> END
  |
  +-- Available
        |
        v
      Validate credit card details
        |
        +-- INVALID --> "There was a problem with your payment." --> END
        |
        +-- VALID
              |
              v
            Authenticate credit card (password check)
              |
              +-- FAILED --> "Credit card authentication failed." --> END
              |
              +-- SUCCESS
                    |
                    v
                  Book the hotel (update CSV)
                    |
                    v
                  User enters their name
                    |
                    v
                  Generate and display reservation ticket
                    |
                    v
                  END
```

---

## Getting Started

### Prerequisites

- **Python 3.x** (3.7 or higher recommended)
- **pandas** library

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/chaitalilangade1/Hotel_Booking_app.git
   cd Hotel_Booking_app
   ```

2. **Install dependencies:**

   ```bash
   pip install pandas
   ```

### Running the Application

```bash
python main.py
```

---

## Usage Guide

1. **View Hotels**: When you run the application, it displays a table of all hotels with their ID, name, city, capacity, and availability status.

2. **Select a Hotel**: Enter the ID of the hotel you wish to book (e.g., `188` for Snow Palace).

3. **Payment Processing**: The application validates the credit card details and authenticates with a password. (Currently, card details are hardcoded in `main.py` for demonstration purposes.)

4. **Booking Confirmation**: If all checks pass, you will be prompted to enter your name. A reservation ticket is then generated and displayed.

---

## Example Walkthrough

**Running the app:**

```
   id                     name        city  capacity available
0  134  Tourist Sunny Apartment   Anchorage         4        no
1  188             Snow Palace   New Delhi         5       yes
2  655          City Break Inn  Porto-Novo         3        no

Enter the id of the hotel: 188
Enter your name: Alice
```

**Output:**

```
        Thank you for your reservation!
        Here are you booking data:
        Name: Alice
        Hotel name: Snow Palace
```

After booking, the `hotels.csv` file is updated to reflect that hotel `188` is no longer available.

---

## Configuration

The application uses CSV files as its data store. To customize the app:

- **Add new hotels**: Add rows to `hotels.csv` following the existing format (`id,name,city,capacity,available`).
- **Add new credit cards**: Add card details to `cards.csv` and corresponding passwords to `card_security.csv`.
- **Reset availability**: Change the `available` column in `hotels.csv` back to `"yes"` to make hotels bookable again.

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

---

*This wiki was generated for the [Hotel_Booking_app](https://github.com/chaitalilangade1/Hotel_Booking_app) repository.*
