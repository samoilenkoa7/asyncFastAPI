# ASYNC LESSON BOOKING SERVICE BASED ON FastAPI

Booking, mailchimp usage and other features will be added soon

## Requirements
- Python>=3.10
- fastapi
- uvicorn
- sqlalchemy
- pydantic[email]
- python-dotenv
- psycopg2-binary
- asyncpg
- alembic
- greenlet
- passlib[bcrypt]
- python-jose
- python-multipart

## Installation
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation.
You can do this by running the command
```
python -m venv venv
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.


Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`auth/sign-in` | POST - to authenticate and get token Bearer
`auth/sign-up` | POST - to create new user and get bearer auth token 
`available-time/get` | GET | READ | Get a single available time for some user 
`available-time/create`| POST | CREATE | Create a new available time
`available-time/delete` | DELETE | DELETE | Delete an available time
...

## Use
We can test the API using [curl](https://curl.haxx.se/) or [httpie](https://github.com/jakubroztocil/httpie#installation), or we can use [Postman](https://www.postman.com/)

Httpie is a user-friendly http client that's written in Python. Let's try and install that.

You can install httpie using pip:
```
pip install httpie
```

First, we have to start up Django's development server.
```
python manage.py runserver
```


## Create users and Tokens

First we need to create a user, so we can log in
```
http POST http://127.0.0.1:8000/auth/sign-up/ 
body = {
  "name": "string",
  "surname": "string",
  "email": "user@example.com",
  "kind": "student",
  "password": "string"
}
```

After we create an account we can use those credentials to get a token

To get a token, if you are already registered first we need to request
```
http http://127.0.0.1:8000/auth/sign-in/
body = {
    username: 'email',
    password: 'password'
}
```
after that, we get the token
```
{
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NzM5MjU4MTgsIm5iZiI6MTY3MzkyNTgxOCwiZXhwIjoxNjczOTI5NDE4LCJzdWIiOiI4NjYzOTA2MzVmNTE0MTkxOWY4ZGM5YmRjNzNmZDg3YSIsInVzZXIiOnsibmFtZSI6IkFydGh1ciIsInN1cm5hbWUiOiJLcnlzaGthIiwiZW1haWwiOiJzYW1vaWxlbmtvYTdAZ21haWwuY29tIiwia2luZCI6InN0dWRlbnQiLCJpZCI6Ijg2NjM5MDYzNWY1MTQxOTE5ZjhkYzliZGM3M2ZkODdhIiwiaXNfYWN0aXZlIjp0cnVlfX0.GVhi8fFHQMGE4TCB2p0DgnzPsED5HYcva4YdDwChuMY'
}
```
We got two tokens, the access token will be used to authenticated all the requests we need to make, this access token will expire after some time.
