# WorkIndia SDE Intern Assignment

## Name: Rohan Gudimetla

## Email: rohan.gudimetla07@gmail.com / rohan21bcs15@iiitkottayam.ac.in

<details>
  <summary><strong>SDE Intern Assignment Details</strong></summary>
Hey there, Mr. X. You have been appointed to design a railway management system like IRCTC, where users can come on the platform and
check if there are any trains available between 2 stations.
The app will also display how many seats are available between any 2 stations and the user can book a seat if the availability > 0 after
logging in. Since this has to be real-time and multiple users can book seats simultaneously, your code must be optimized enough to handle
large traffic and should not fail while doing any bookings.
If more than 1 users simultaneously try to book seats, only either one of the users should be able to book. Handle such race conditions
while booking.
There is a Role Based Access provision and 2 types of users would exist :
1. Admin - can perform all operations like adding trains, updating total seats in a train, etc.
2. Login users - can check availability of trains, seat availability, book seats, get booking details, etc.
Tech Stack:
1. Any web server of your choice (Python Flask / Django, NodeJS / ExpressJS , Java/Springboot, etc)
2. Database: MySQL/PostgreSQL (Compulsory)

</details>

## Tech Stack

- **Python**
- **Django**
- **PostgreSQL**
- **Celery**
- **Redis**
- **Black**

## How to setup and run locally (With Docker)

1. **Clone the repository:**

```bash
   git clone git@github.com:roanster007/bharatfd.git
```

2. **Rename `.env.dev` to `.env`**

3. **Disable any postgres instance running locally (Sometimes it interrupts with the one in the Docker Image)**

```bash
sudo systemctl stop postgresql
```

3. **Build the docker image:**

```bash
   docker-compose build
```

This will install all the requirements, and build the Docker image.

4. **Run the Docker container**:

```bash
docker-compose up
```

This will spin up the server. The API is accessible at `localhost:8000`.

## Architecture

1. A user can make requests as per the API endpoints described below.
2. A user can choose a source and destination of trip and can get list of trains available between the source and destination, with at least one ticket.
   -- For simplicity purposes, each station the train travels to is assumed to be an index in range **[0, n]**, where n is the maximum destination index among destination of all trains.
   -- **source < destination** for all the trains.
3. Then, a user can choose to book certain number of seats for a particular train id. In return, a user gets a **Booking ID**, and user's request is added to a processing queue in **Redis**, which is picked up and processed by **Celery** Workers.
4. The **Booking ID** servers as a medium, through which users can check whether their Booking is `CONFIRMED`, `PENDING`, OR `CANCELLED`.
5. Offloading processing to **Celery** makes jobs asynchronous and reduces load on server.
   **NOTE that database rows are locked while updating Booking rows for processing ticket, preventing RACES.**

6. Towards the Admin Panel, admins can use an existing API Key, and add new trains between two points, and number of seats it has. They can also get list of all the operating stations.

## API Endpoints

## **1. User Registration (`/register`)**

### **Method:** `POST`

Registers a new user using email and password.

### **Request Format**

- **Content-Type:** `application/x-www-form-urlencoded`
- **Body Parameters:**
  - `email` (string, required) – User's email address.
  - `password` (string, required) – User's password.

### **Example Request**

```bash
curl -X POST "http://localhost:8000/register" \
     -d "email=a@gmail.com&password=hello" \
     -H "Content-Type: application/x-www-form-urlencoded"
```

response:

```bash
{
   "success": "Successfully registered! Please login to get auth token!"
}
```

## **1. User Registration (`/register`)**

### **Method:** `POST`

Registers a new user using email and password.

### **Request Format**

- **Content-Type:** `application/x-www-form-urlencoded`
- **Body Parameters:**
  - `email` (string, required) – User's email address.
  - `password` (string, required) – User's password.

### **Example Request**

```bash
curl -X POST "http://localhost:8000/register"      -d "email=a@gmail.com&password=hello"      -H "Content-Type: application/x-www-form-urlencoded"
```

### **Response**

```json
{
  "success": "Successfully registered! Please login to get auth token!"
}
```

---

## **2. User Login (`/login`)**

### **Method:** `GET`

Logs in a user using email and password, returning an authentication token.

### **Request Format**

- **Query Parameters:**
  - `email` (string, required) – User's email address.
  - `password` (string, required) – User's password.

### **Example Request**

```bash
curl -X GET "http://localhost:8000/login?email=a@gmail.com&password=hello"
```

### **Response**

```json
{
  "success": "Successful Login! Auth Token - 39896666"
}
```

---

## **3. Booking Status (`/booking`)**

### **Method:** `GET`

Retrieves booking status using `auth_token` and `booking_id`.

### **Request Format**

- **Query Parameters:**
  - `auth_token` (string, required) – User's authentication token.
  - `booking_id` (integer, required) – ID of the booking.

### **Example Request**

```bash
curl -X GET "http://localhost:8000/booking?auth_token=39896666&booking_id=5"
```

### **Response**

```json
{
  "user_id": 1,
  "train": 1,
  "source": 0,
  "destination": 1,
  "seats": 1,
  "status": 1,
  "id": 5
}
```

---

### **Method:** `POST`

Books a ticket. Booking is added to a queue and processed asynchronously.

### **Request Format**

- **Content-Type:** `application/x-www-form-urlencoded`
- **Body Parameters:**
  - `auth_token` (string, required) – User's authentication token.
  - `train_id` (integer, required) – Train ID for booking.
  - `source` (integer, required) – Source station index.
  - `destination` (integer, required) – Destination station index.
  - `seats` (integer, required) – Number of seats to book.

### **Example Request**

```bash
curl -X POST "http://localhost:8000/booking"      -H "Content-Type: application/x-www-form-urlencoded"      -d "auth_token=39896666&train_id=1&source=0&destination=1&seats=1"
```

### **Response**

```json
{
  "success": "Your booking id 5 is in process. Please check the status after some time using the id."
}
```

---

## **4. Seat Availability (`/seats`)**

### **Method:** `GET`

Fetches available seats for a given route.

### **Request Format**

- **Query Parameters:**
  - `source` (integer, required) – Source station index.
  - `destination` (integer, required) – Destination station index.

### **Example Request**

```bash
curl -X GET "http://localhost:8000/seats?source=0&destination=1"
```

### **Response**

```json
{
  "trains": [
    {
      "id": 1,
      "source": 0,
      "destination": 1,
      "seats": 50,
      "booked_seats": 41
    },
    {
      "id": 2,
      "source": 0,
      "destination": 1,
      "seats": 50,
      "booked_seats": 30
    }
  ]
}
```

---

## **5. Train Management (`/administration`)**

- **ADMIN API KEY** - `DEF123`

### **Method:** `POST`

Adds a new train. Requires an API key for authentication.

### **Request Format**

- **Content-Type:** `application/x-www-form-urlencoded`
- **Body Parameters:**
  - `API_KEY` (string, required) – Admin API key.
  - `source` (integer, required) – Source station index.
  - `destination` (integer, required) – Destination station index.
  - `seats` (integer, required) – Number of available seats.

### **Example Request**

```bash
curl -X POST "http://localhost:8000/administration"      -H "Content-Type: application/x-www-form-urlencoded"      -d "API_KEY=DEF123&source=1&destination=2&seats=50"
```

### **Response**

```json
{
  "success": "Train successfully added"
}
```

### **Method:** `GET`

Fetches list of all the trains running.

### **Request Format**

- **Query Parameters:**
  - `API_KEY` (string, required) – Admin API key.

### **Example Request**

```bash
curl -X GET "http://localhost:8000/administartion?API_KEY=DEF123"
```

### **Response**

```json
{
  "trains": [
    {
      "id": 1,
      "source": 0,
      "destination": 1,
      "seats": 50
    },
    {
      "id": 2,
      "source": 0,
      "destination": 1,
      "seats": 50
    },
    {
      "id": 3,
      "source": 1,
      "destination": 2,
      "seats": 50
    }
  ]
}
```
