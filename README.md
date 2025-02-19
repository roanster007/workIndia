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

- **Language**: Python
- **Framework**: Django
- **Database**: PostgreSQL
- **Celery**
- **Message Broker**: Redis
- **Formatting**: Black

## How to setup and run locally (With Docker)

1. **Clone the repository:**

```bash
   git clone git@github.com:roanster007/bharatfd.git
```

2. **Rename `.env.dev` to `.env`**

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

## Troubleshooting

- Please terminate any locally running Postges instance in case it is running, since sometimes it seems to interfere with the one running in the container.

## API Endpoints

1. `register`:

- **POST**: Used to register a user using email and password.

example:

```bash
localhost:8000/register?email=a@gmail.com&password=hello
```

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

2. `login`:

- **GET**: Logs in user using email id and password, and returns and Authorization token using which they can book tickets, or check booking status.

example:

```bash
localhost:8000/login?email=a@gmail.com&password=hello
```

```bash
curl -X GET "http://localhost:8000/login?email=a@gmail.com&password=hello"
```

response:

```bash
{
    "success": "Successful Login! Auth Token - 39896666"
}
```

3. `booking`:

- **GET**: Used to get booking status. Takes in auth token of user and booking id.

example:

```bash
localhost:8000/booking?auth_token=39896666&booking_id=5
```

```bash
curl -X GET "http://localhost:8000/booking?auth_token=39896666&booking_id=5"
```

response:

```bash
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

- **POST**:
  -- Used to book ticket. Takes in `train_id`, `source`, `destination`, `seats` (number of seats to book) and `auth token`, and returns booking id to check status of booking.

-- Note that booking is not immediately processed -- it is first added to the Booking Processing Queue, from where it is picked up by a Celery Worker Asynchronously and processed. Hence, a booking id is returned to users, using which they can keep checking booking status.

example:

```bash
localhost:8000/booking?auth_token=39896666&train_id=1&source=0&destination=1&seats=1
```

```bash
curl -X POST "http://localhost:8000/booking" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "auth_token=39896666&train_id=1&source=0&destination=1&seats=1"
```

response:

```bash
{
    "success": "Your booking id 5 is in process. Please check the status after some time using the id."
}
```

4. `administration`:

- **POST**:
  -- Takes in API Key which is available with Admin authorities only, and use it to add new train by passing `source`, `destination`, and `seats` parameters.
  -- Initial API Key can be assumed to be `INITIAL_API_KEY = "DEF123"`

example:

```bash
localhost:8000/administartion?API_KEY=DEF123&source=1&destination=2&seats=50
```

```bash
curl -X POST "http://localhost:8000/administartion" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "API_KEY=DEF123&source=1&destination=2&seats=50"

```

response:

```bash
{
    "success": "Train successfully added"
}
```
