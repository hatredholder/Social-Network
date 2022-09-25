# Pybook - Social Network

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

1. Clone this repository, cd into it

```
git clone https://github.com/hatredholder/Social-Network.git
cd Social-Network
```    

2. Start a new **Virtualenv**, activate it, install Python module requirements

```
virtualenv myenv
source myenv/bin/activate
pip install -r requirements.txt
```  
3. Create a **PostgreSQL** database

```
CREATE DATABASE socialnetworkdb;
```

4. Create a **.env** file with enviroment variables of `APP_SECRET, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT`

```
APP_SECRET=123
DB_NAME=socialnetworkdb
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
``` 

5. Apply migrations to the database and run the **Django** server 

```
python manage.py migrate 
python manage.py runserver
```  

## Technologies

Frontend: CSS, Semantic UI 2.4.

Backend: Django 4.0, JavaScript and AJAX.

Database: PostgreSQL.

# To Do/To Add

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
