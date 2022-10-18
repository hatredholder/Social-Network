# Pybook - Social Network 

![Pytest](https://github.com/hatredholder/Social-Network/workflows/tests/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/hatredholder/Social-Network/badge.svg?branch=main)](https://coveralls.io/github/hatredholder/Social-Network?branch=main)

:earth_americas: :earth_americas: :earth_americas:

A Social Network type of project called Pybook written in **Django**.

## Features

- Authentication
- Adding as a Friend
- Post Feed
- Profile Pages
- Messaging between Users
- Like and Comment on Posts
- Notifications on Friend Requests
- Search Users

## Preview

![social_network](https://user-images.githubusercontent.com/86254474/175503144-70b07513-1a24-400a-80ce-bd8669167660.png)

## Instructions

Clone this repository, cd into it

```
git clone https://github.com/hatredholder/Social-Network.git
cd Social-Network
```    

Start a new **Virtualenv**, activate it, install Python module requirements on it

```
virtualenv myenv
source myenv/bin/activate
pip install -r requirements/base.txt
```  
Create a **PostgreSQL** database

```
CREATE DATABASE socialnetworkdb;
```

Create a **.env** file with enviroment variables of `APP_SECRET, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT`

```
APP_SECRET=your_very_very_secure_secret_key
DB_NAME=socialnetworkdb
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
``` 

Apply migrations to the database and run the **Django** server 

```
python manage.py migrate 
python manage.py runserver
```  

## Testing

To use the tests you need to install **local** module requirements first, to do that, use:
```
pip install -r requirements/local.txt
```

To run the tests and check the coverage use:
```
pytest --cov
```

To generate an HTML coverage report use:
```
pytest --cov-report html:cov_html --cov
```

And finally to test the code quality (see if there are any PEP8 errors) use:
```
flake8
```

## Technologies

Frontend: CSS, Semantic UI 2.4.

Backend: Django 4.1, JavaScript and AJAX.

Database: PostgreSQL.

## To Do/To Add

- [x] Add 100% coverage tests;

- [x] Add followers count to profile detail;

- [x] Move to a local database instead of a online server;

- [x] Make navbar sticky;

- [x] Refactor all code (add comments everywhere they're needed, make sure all code is formatted by PEP8);

- [x] Add delete comment functionality; 

- [x] Add messenger/chat functionality;

- [x] Add search bar functionality;

- [x] Add follow user functionality;

- [x] Hide posts of people that user doesn't follow/didn't add as a friend;

- [x] Add a welcome page for non-authorized users;
