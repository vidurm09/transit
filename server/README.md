[How to activate the environment](https://flask.palletsprojects.com/en/3.0.x/installation/#activate-the-environment)

Run the server with `flask --app server run`

Run the server for prod with `gunicorn -w 1 -b 0.0.0.0 "server:app"`