# STEPS to setup project
```markdown
1. `git clone https://github.com/python10sep/tracker.git`
2. If project already exists - `git pull origin main` (provided `git remote -v` should point to correct upstream)
3. create and activate `venv`
4. `pip install -r requirements.txt` (pytest, motor, pytest-asyncio, fastapi)
5. navigate to project root and run `docker-compose up -d`
6. `docker ps` (capture container name from here)
7. `docker exec -it tracker-mongo-1 mongosh`
8. `pytest .`
```

NOTE - 
- Those who do NOT have docker can directly install mongo and execute `mongosh`



## How to understand test cases?
- We run all the test cases using `pytest .` command
- To understand each test case we can add `breakpoint()` in respective test cases
- And simultaneously, in another tab we can run `mongosh`
- Docker users can run `docker exec -it tracker-mongo-1 mongosh`
- Non-docker users can `mongosh`
- Use following mongo commands
```markdown
- `show databases`
- `use my-database`
- `show collections`
- `db.films.find()`
```