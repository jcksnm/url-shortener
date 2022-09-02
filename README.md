# url-shortener

## Overview
This is python web application that shortens URL.

## Technologies Used
Backend: Python

Database: SQLite

API: FastAPI

Web Server: Uvicorn

## Instructions

### 1. Create a python virtual environment
```
$ virtualenv env
$ source env/bin/activate
(env) $
```

### 2. Install requirements
```
(env) $ python -m pip install -r requirements.txt
```

### 3. Run project 
```
(env) $ uvicorn shortener_app.main:app --reload
```

## Credits
This project was made using a tutorial from Philipp Acsany on realpython.com

Link: https://realpython.com/build-a-python-url-shortener-with-fastapi/
