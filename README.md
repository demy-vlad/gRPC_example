## Installation
```bash
bash:

python3 -m venv venv
# use correct version of Python when creating VENV
# OR
py -m venv venv
# use correct version of Python when creating VENV

pip install -r requirements.txt
# install requirements
```

## Run server
```bash
python3 app\auth_server.py
# OR
py app\auth_server.py

```

## Run tests
```bash
pytest
# OR
pytest -m "xfail"
```