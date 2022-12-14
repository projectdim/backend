## Project installation

Install the requirements
```
pip install -r requirements.txt
```

Create a new file - `.env` in the root folder of the project and fill it out the same as `.env.example`

-----------------------------------------------

## Shell script (Option 1)

On windows - just type the following to the command line of your IDE:
```
pre_start.sh
```

On Unix systems - type this:
```
/usr/bin/bash pre_start.sh
```

------------------------------------------------
## Default (Option 2)

Next up, create the db (requires postgresSQL installed) with:

```
alembic upgrade heads
```


If you have changed any models (or made any changes that require migrating the db) run:
```
alembic revision --autogenerate -m "Note text"
```

You might need to enter env for this (not sure) :

On unix systems :
```
source venv/bin/activate
```

On windows :
```
venv/Scripts/activate.bat
```

------------------------

Run the `populate_db.py` file in the root of the project

```
python populate_db.py
```

Run the tests with :
```
pytest 
```
---------------------------------
## Run the project with :
```
uvicorn app.main:app --reload --port 7000
```

You can access the docs by this [Link](http://127.0.0.1:7000/docs)