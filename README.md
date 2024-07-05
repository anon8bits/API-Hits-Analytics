
# API Management Dashboard

This ia a web application that effectively tracks API hits, stores them in a PostgreSQL database, and presents insightful visualizations on a separate dashboard. This project will provide valuable insights into API usage patterns and trends, facilitating informed decision-making.



## Demo

https://t.ly/9Z8YO


## Run Locally

Before starting, make sure you have PostgreSQL installed in your system and has a database to work upon. Clone the project

```bash
  git clone https://github.com/anon8bits/API-Hits-Analytics
```

Go to the Backend directory

```bash
  cd Backend
```

Install dependencies

```bash
  pip install -r requirements.txt
```
Create an .env file file and declare your Postgres connection URI.

```bash
  POSTGRES_URI = [PUT YOUR URI HERE]
```
Create a .flaskenv file for flask configurations 

```bash
  FLASK_APP = app
  FLASK_DEBUG = 1
```

Start the backend server

```bash
  python app.py
```
or

```bash
  flask run
```
Go to the Frotnend directory

```bash
  cd Frotnend/api-dashboard
```
Install required dependencies

```bash
  npm install
```
Start the react app

```bash
  npm run start
```

Now you can view all the API endpoints analytics on the same page.


