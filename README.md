# AirTicket Booking Flight Platform
Welcome to AirTicket, your convenient and reliable platform for booking flights effortlessly! Whether you're planning a business trip, a family vacation, or a spontaneous getaway, AirTicket has got you covered.


## Getting Started

1. Clone the Repository:

   ```bash
   git clone https://github.com/Maks-Siglov/Air-Ticket.git
   cd Air-Ticket/
   ```

2. Create `air_ticket` postgres db.
    - **Example data in .env.docker_db:**
    ```bash
    DB_NAME=air_ticket
    DB_USER=admin
    DB_PASSWORD=admin
    DB_HOST=localhost
    DB_PORT=5432
    ``` 

## Start With Docker


1. Establish user

    ```bash
      source env.sh
     ```

2. Create docker network

    ```bash
      docker network create mynetwork  
     ```

3. Build app 
    ```bash
      docker compose build  
     ```

4. Start services 
    ```bash
      docker compose up  
     ```
   
5.  Visit `http://127.0.0.1:8080/`

6. Now you can log in as Admin user or continue exploring without login
   ```bash
      login: admin@gmail.com
      password: admin_user22 
   ```

7. See Enable Extended Functionality for enable sending email notification


## Run Locally

1. Install dependencies:

    ```bash
    pip install -r requirements/prod.txt -r requirements/tools.txt -r requirements/dev.txt
    ```

2. Create postgres db and place data to the .env.local file:
    - **Example data in .env.local:**
    ```bash
    DB_NAME=air_ticket
    DB_USER=admin
    DB_PASSWORD=admin
    DB_HOST=localhost
    DB_PORT=5432
    ```

3. Apply migrations:

    ```bash
    cd air_ticket/
    python manage.py migrate
    ```

4. Load Dumpdata:
    - **Right now Dumpdata provides only flights on 3 march into Berlin. Example for search in main page from Vienna to Berlin in 1 april**
    ```bash
    python manage.py loaddata fixtures/*
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

6. Visit `http://127.0.0.1:8000/`

## Enable Extended Functionality

1. Project use email for sending message with user credentials and order details. For using this feature add your email data in .env.local file
    - **Replace data in .env.local / .env.docker  file**
     ```bash
    EMAIL_HOST=smtp.gmail.com /or another smtp
    EMAIL_PORT=587
    EMAIL_HOST_USER=Replace with your email
    EMAIL_HOST_PASSWORD=Replace with your app password
    ```

2. For providing payment functionality you need the stripe API keys
    - **Replace data in .env files**
     ```bash
    STRIPE_PUBLIC_KEY=Place your stripe public key here
    STRIPE_SECRET_KEY=Place your stripe secret key here
    ```


## Using Process

1. First, the user fills out a form with their flight details (from and to locations) and the number of passengers:

   ![Main page](https://raw.githubusercontent.com/Maks-Siglov/Air-Ticket/air_ticket/static/images/screenshots/start_page.png)

2. After filling out the form, the user can view available flights:

   ![Flights](https://raw.githubusercontent.com/Maks-Siglov/Air-Ticket/air_ticket/static/images/screenshots/searched_flights.png)

3. The user then selects a flight and fills in the ticket and contact information:

   ![Fill ticket data](https://raw.githubusercontent.com/Maks-Siglov/Air-Ticket/air_ticket/static/images/screenshots/fill_ticket_data.png)

4. The user is redirected to the Stripe payment system. After successful payment, they receive an email with their login credentials and are redirected to view their ticket information:

   ![Tickets data](https://raw.githubusercontent.com/Maks-Siglov/Air-Ticket/air_ticket/static/images/screenshots/tickets.png)

5. The user can go to their profile, where they can change their password, update contact information, search for their orders, flights, and check-in:

    ![Profile](https://raw.githubusercontent.com/Maks-Siglov/Air-Ticket/air_ticket/static/images/screenshots/profile.png)

6. The user can check in for their flight and choose their desired seat using an interactive seat map:

   ![Seat map](https://raw.githubusercontent.com/Maks-Siglov/Air-Ticket/air_ticket/static/images/screenshots/check_in_seat_map.png)