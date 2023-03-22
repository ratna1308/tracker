# STEPS to setup project
```markdown
1. `git clone https://github.com/python10sep/tracker.git`
2. If project already exists - `git pull origin main` (provided `git remote -v` should point to correct upstream)
3. create and activate `venv`
4. `pip install -r requirements.txt` (pytest, motor, pytest-asyncio, fastapi)
5. navigate to project root and run `docker-compose up -d`
6. `docker ps` (capture container name from here)
7. `docker exec -it <container-name> mongosh`
8. `pytest .`
```

NOTE - 
- Those who do NOT have docker can directly install mongo and execute `mongosh`
