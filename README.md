## Project installation

Install the requirements
```
pip install -r requirements.txt
```

Create a new file - `.env` in the root folder of the project and fill it out the same as `.env.example`


Next up, create the db (requires postgresSQL installed) with:

```
alembic upgrade heads
```


If you have changed any models (or made any changes that require migrating the db) run:
```
alembic revision --autogenerate -m "Note text"
```

Run the `populate_db.py` file in the root of the project
```
python -m populate_db.py
```

Run the tests with :
```
pytest 
```

Run the project with :
```
uvicorn app.main:app --reload --port 7000
```

You can access the docs by this [Link](http://127.0.0.1:7000/docs)