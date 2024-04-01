# AirTicket Booking Flight Platform
Welcome to AirTicket, your convenient and reliable platform for booking flights effortlessly! Whether you're planning a business trip, a family vacation, or a spontaneous getaway, AirTicket has got you covered.


## Getting Started

Clone the Repository:

```bash
git clone https://git.foxminded.ua/foxstudent105590/task_19_air_crm.git
cd task_19_air_crm/
```

## Start With Docker


1. Establish docker user

    ```bash
      source env.sh
     ```

2. Create docker network

    ```bash
      docker network create mynetwork  
     ```

3. Start services 
    ```bash
      docker compose up  
     ```

4. See Enable Extended Functionality for enable sending email notification


## Run Locally

1. Install dependencies:

    ```bash
    pip install -r requirements/prod.txt -r requirements/tools.txt -r requirements/dev.txt
    ```

2. Create postgres db and place data to the .env.local file:
    - **Example data in .env.local:**
    ```bash
    DB_NAME='air_ticket'
    DB_USER='admin'
    DB_PASSWORD='admin'
    DB_HOST='localhost'
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
    - **Replace data in .env.local file**
     ```bash
    EMAIL_HOST='smtp.gmail.com /or another smtp'
    EMAIL_PORT=587
    EMAIL_HOST_USER='Replace with your email'
    EMAIL_HOST_PASSWORD='Replace with your app password'    
    ```
   