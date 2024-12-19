[How to activate the environment](https://flask.palletsprojects.com/en/3.0.x/installation/#activate-the-environment)

Run the server with `flask --app server run`

Run the server for prod with `gunicorn -w 1 "server:app"` with nginx setup correctly

run on start up with `sudo systemctl enable transit.service` based on https://www.tderflinger.com/en/deploy-flask-gunicorn-nginx-systemd-raspberrypi

Example NGINX config 
```
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Prefix /;
    }
}
```