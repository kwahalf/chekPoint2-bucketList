[![Build Status](https://travis-ci.org/kwahalf/chekPoint2-bucketList.svg?branch=develop)](https://travis-ci.org/kwahalf/chekPoint2-bucketList)
[![Coverage Status](https://coveralls.io/repos/github/kwahalf/chekPoint2-bucketList/badge.svg?branch=develop)](https://coveralls.io/github/kwahalf/chekPoint2-bucketList?branch=develop)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)
# Bucketlist API
According to Merriam-Webster Dictionary,  a Bucket List is a list of things that one has not done before but wants to do before dying.

This is an online flask API built to help users keep track of their things to do

## Installation and Setup
Clone the repo
```
https://github.com/kwahalf/chekpoint2-bucketlist.git
```
Navigate to the root folder
```
cd chekpoint2-bucketlist
```
create a virtualenv 
```
virtualenv --python=python3 bucketenv
```
activate virtualenv and export the environment variables by running the following
```
source .env
```
Install the requirements
```
pip install -r requirements.txt
```
Create the main and the test database from the command line by running the script:
```
$ createdb flask_api
$ createdb test_db

```
Initialize, migrate, upgrade the datatbase
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
## Launch the progam
Run 
```
python manage.py runserver
```
Interact with the API, send http requests using Postman or alternatively use the documentation to test it out by pasting
the the url being served by the development server on your browser and off you go
## API Endpoints
| URL Endpoint | HTTP Methods | Summary |
| -------- | ------------- | --------- |
| `/auth/register/` | `POST`  | Register a new user|
|  `/auth/login/` | `POST` | Login and retrieve token|
| `/bucketlists/` | `POST` | Create a new Bucketlist |
| `/bucketlists/` | `GET` | Retrieve all bucketlists for user |
| `/bucketlists/?page=1&limit=3/` | `GET` | Retrieve three bucketlists per page |
 `/bucketlists/?q=name/` | `GET` | searches a bucketlist by the name|
| `/bucketlists/<id>/` | `GET` |  Retrieve a bucketlist by ID|
| `/bucketlists/<id>/` | `PUT` | Update a bucketlist |
| `/bucketlists/<id>/` | `DELETE` | Delete a bucketlist |
| `/bucketlists/<id>/items/` | `POST` |  Create items in a bucketlist |
| `/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete an item in a bucketlist|
| `/bucketlists/<id>/items/<item_id>/` | `PUT`| update a bucketlist item details|

## Testing
You can run the tests ``` python manage.py runserver

