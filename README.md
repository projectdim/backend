## Project installation

```
pip install -r requirements.txt
```

After installing the requirements, create an fill out the .env file.
Next up, create the db (requires postgreSQL installed) with:

```
alembic upgrade heads
```

If you have changed any models (or made any changes that require migrating the db) run:
```
alembic revision --autogenerate -m "Note text"
```

Run the project with :
```
uvicorn app.main:app --reload --port 7000
```

You can access the docs by this [Link](http://127.0.0.1:7000/docs)