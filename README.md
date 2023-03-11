## STEPS
- create new project named `tracker`
- `pip install "fastapi[all]"`
- `pip freeze > requirements.txt`
- `pip freeze > requirements.dev.txt`
- `pip freeze > requirements.test.txt`


## Project structure

STEP 1
```
tracker  (project root)
├── README.md
├── api
│   ├── __init__.py
│   └── api.py  (sub-application)
├── main.py
├── requirements.dev.txt
├── requirements.test.txt
├── requirements.txt

```

STEP 2
```

tracker
├── README.md
├── api
│   ├── __init__.py
│   ├── api.py
│   └── handlers
│       ├── __init__.py
│       └── demo.py
├── main.py
├── requirements.dev.txt
├── requirements.test.txt
├── requirements.txt

```


#### Re-organize order of imports
```bash
pip install isort

# navigate to project root dir
isort .
```

#### format code
```bash

pip install black
# navigate to project root dir
black .
```

#### To remove unused imports and unused variables
```bash

pip install autoflake
# navigate to project root dir
autofautoflake --in-place -r .
```

## To run make file

```bash
make fmt
```




# MONGO SETUP

## To start Mongo shell

At start, add `docker-compose.yaml` file in your project root.
And then run following commands - 
```bash

# execute following command for the first time
docker-compose up -d mongo

# To list all running containers
docker ps

# execute following command for the next time
docker exec -it tracker-mongo-1 mongosh

# In above command `tracker-mongo-1` should be name that reflects in `docker ps`
```
