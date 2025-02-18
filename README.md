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
- **Caching**: Redis
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
