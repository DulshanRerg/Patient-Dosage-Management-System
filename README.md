# Dose Tracking System

This project is a Django-based web application for tracking patient dosages, managing medicines, and facilitating communication between doctors and patients.

## Features

- Doctor registration and login
- Email verification for doctor accounts
- Dashboard for managing patients, medicines, and dosages
- Assign dosages to patients
- Send messages to patients
- Track dosage status

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/dose-tracking.git
    cd dose-tracking
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```sh
    python manage.py migrate
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

6. Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

- Register as a doctor and verify your email.
- Log in to access the dashboard.
- Add patients and medicines.
- Assign dosages to patients.
- Send messages to patients.

## Developer Information

- Name: Abdul Shaban Rajabu
- Email: [dulshanrerg01@duck.com]


## License

This project is licensed under the MIT License. See the LICENSE file for details.