#! /usr/bin/env bash

#activate venv
source venv/bin/activate

#install the requirements
pip install -r requirements.txt

#run migrations
alembic upgrade heads

#create initial data in db
python populate_db.py

echo "Running tests"

sleep 5

#run tests
python -m pytest

#exit venv
deactivate
