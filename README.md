# The API

## Running some commands for the project creation
```
python -m venv .venv
```

So we initialized our virtual environment.

And running it:
```
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the server in local
```
uvicorn app.main:app --reload
```
