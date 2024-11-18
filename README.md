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

## How to add new dependencies

```shell
source .venv/bin/activate
pip install python-jose[cryptography]
pip freeze > requirements.txt
```
## How to deploy to Heroku.com?
![image](https://github.com/user-attachments/assets/3b282a00-111b-4326-af10-0161a9955c30)
![image](https://github.com/user-attachments/assets/949934ea-195a-499f-be1e-38f491663cbb)

For more details visit https://jnikenoueba.medium.com/how-to-deploy-a-fastapi-api-on-heroku-7d805cb83ffa

