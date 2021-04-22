## About the app

The main aim of this application is to create simple concert API using Python Flask and SQL Alchemy

# Activate venv

\$ pipenv shell

# Install dependencies

\$ pipenv install

# Create DB

\$ python

> > from app import db
> > db.create_all()
> > exit()

# Run Server (http://localhst:5000)

python App.py

## Endpoints

1. GET /concert
2. POST /concert
3. GET /concert/:id
4. PUT /concert/:id
5. DELETE /concert/:id
6. PATCH /concert/:id
