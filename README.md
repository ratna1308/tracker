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

Step 3
```markdown
tracker
├── Makefile
├── README.md
├── api   # sub-application to be mounted on main application
│   ├── __init__.py
│   ├── _tests
│   │   ├── __init__.py
│   │   ├── fixtures.py
│   │   └── repository
│   │       ├── __init__.py
│   │       └── film
│   ├── api.py   # application instantiation
│   ├── entities  # defines a new resource / entity in the project
│   │   ├── __init__.py
│   │   └── film.py
│   ├── handlers  # sample demo application for CRUD operations
│   │   ├── __init__.py
│   │   └── demo.py
│   ├── repository   # defines DB access to each resource
│   │   ├── __init__.py
│   │   └── film   # resource
│   │       ├── __init__.py
│   │       ├── abstractions.py
│   │       ├── memory.py
│   │       └── mongo.py
│   └── responses
│       ├── __init__.py
│       └── detail.py
├── docker-compose.yaml
├── films.json
├── main.py    # entrypoint
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

NOTE - 
If `mongosh` command is not working for non-docker users then they need 
to set up PATH variable. Refer - https://www.mongodb.com/docs/mongodb-shell/install/#install-from-.zip-file


# MONGO Commands

#### To get list of existing databases
```bash
show databases
```
#### To get help
```bash
.help
```
#### To use existing or create new database
```bash
use films
```
#### To insert a single record in database
```bash
db.films.insertOne({"title": "My Film", "year": 2023, "watched": false})
```

#### To get list of all the records in given table
```bash
db.films.find()
```

#### To get single record (by default this command returns the oldest record)
```bash
db.films.findOne()
```

#### To filter out records based on certain column
```bash
db.films.find({"title": "My Film"})
db.films.find({"year": 2023})
```

#### To filter out records based id
```bash
db.films.findOne({"_id": ObjectId("640c62845792975afc98eb32")})
```

#### To get records in descending order
```bash
db.films.find().sort({"year": -1})
```

#### To get only certain fields from any given record
```bash
db.films.find({}, {"title": 1, "year": 1})
```

#### To exclude certain field in output
```bash
db.films.find({}, {"title": 0})

```

NOTE - we cannot use selection and exclusion in same query.
For example it will be invalid to say - `db.films.find({}, {"title": 1, "year": 0})`

#### To insert multiple films in single shot
```bash
db.films.insertMany() # list of films should be provided as input
db.films.insertMany([{"title":"spiderman","year":2018,"watched":false},{"title":"avengers","year":2022,"watched":false},{"title":"starwars","year":2023,"watched":true},{"title":"randomfilm","year":2001,"watched":true}])
```

#### To get films produced before/after 2021
```bash
db.films.findOne({"year": {"$gt": 2021}})
db.films.find({"year": {"$gt": 2021}})
db.films.findOne({"year": {"$lt": 2021}})
db.films.find({"year": {"$lt": 2021}})
```

#### To get count of records
```bash
db.films.countDocuments()
```

#### To get all the films but skip 1 
```bash
db.films.find().skip(1)  # oldest record is skipped
```


#### To delete a record
```bash
db.films.deleteOne({"_id": ObjectId("640c62845792975afc98eb31")})
```
#### To update records
```bash
db.films.updateOne({"_id": ObjectId("640c62845792975afc98eb33")}, {$set: {"year": 2018}})
```


#### Pros of pytest/Cons of unittest:
- pytest requires essentially no boilerplate as in no classes, setUp, and tearDown methods. All tests are simple functions.
- It uses standard assert statements as opposed to learning and using specific methods, e.g., self.assertEqual or assertDictContainsSubset.
- Fixtures are automagically injected into the different tests meaning they can be used across different tests without being re-implemented across different test-cases or having to be implemented in a different module and manually imported into individual test-cases. 
- This also allows for very easy composition of fixtures into specific tests. 
- Has built-in support for JUnit output to be used in CI tools (Jenkins, SonarQube) without requiring an additional dependency e.g. unittest-xml-reporting. 
- It allows for tests to be 'tagged' through markers, e.g., tests can be tagged as 'api', 'db', 'invoice', and allows for running only tests tagged as X making selecting testing easier. 
- It allows for easy parametrization of tests and shows the result of each sub-test without requiring loops 
- Allows for gradual migration as the pytest runner supports unittest so existing codebases don't need to be ported immediately. 
- It is new-n-shiny (TM).

#### Pros of unittest/Cons of pytest:
- We have been using unittest forever and have a large codebase using it. 
- It is included in the stdlib while pytest would be yet-another-requirement (YAR).
- It has some advanced assertion methods that would need to be redone with standard asserts, e.g., remaking assertDictContainsSubset or remaking assertAlmostEqual, that may be cumbersome to replace.
- Careless definition of fixtures may make it hard for a developer to figure out where they're coming from as they don't need to be defined in the module they're being used.
- Local Development
