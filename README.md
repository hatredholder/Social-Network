<h1 align="center">Pybook - Social Network</h1>

<div align="center">
    	<a href="#-features">Features</a>
  <span> • </span>
       	<a href="#-preview">Preview</a>
  <span> • </span>
  	<a href="#-instructions">Instructions</a>
  <span> • </span>
	<a href="#-testing">Testing</a>
  <span> • </span>
	<a href="#-technologies">Technologies</a>
  <span> • </span>
	<a href="#-to-do">To Do</a>
  <p></p>
</div> 

<div align="center">

![Pytest](https://github.com/hatredholder/Social-Network/workflows/tests/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/hatredholder/Social-Network/badge.svg?branch=main)](https://coveralls.io/github/hatredholder/Social-Network?branch=main)

An open-source Social Network project called Pybook written in **Django**.

</div> 

## ✨ Features

- Authentication
- Adding as a Friend
- Post Feed
- Profile Pages
- Messaging between Users
- Like and Comment on Posts
- Notifications on Friend Requests
- Search Users

## 🔎 Preview

![image](https://user-images.githubusercontent.com/86254474/201476598-c993186c-8f29-465c-b9e4-0cab2abe5530.png)

## 📖 Instructions

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

## 🧪 Testing

To use the **tests** you need to install **local** module requirements first, to do that, use:
```
pip install -r requirements/local.txt
```

To run the **tests** and check the **coverage** use:
```
pytest --cov
```

To generate an HTML **coverage** report use:
```
pytest --cov-report html:cov_html --cov
```

And finally to test the **code quality** (see if there are any PEP8 errors) use:
```
flake8
```

## 💻 Technologies

Frontend: **CSS**, **Semantic UI**

Backend: **Django**, a tiny bit of **JavaScript**

Database: **PostgreSQL**

Tests: **Pytest**, **Pytest-Django**

## 📋 To Do

<details>

  <summary>Click to Open</summary>

- [x] Update comment delete button;

- [x] Add comments form to profile detail view;

- [x] Change messenger url from pk to slug;

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

</details>
