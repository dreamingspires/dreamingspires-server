## Running the development server
`dreamingspires-server` has its dependencies managed by the [poetry](https://python-poetry.org) build system.  To get started, install poetry.

Build the submodules:
```
cd modules/flask-navigation
python3 setup.py bdist_wheel
```

Within the repo, run:

```
poetry install
```

To run the project within poetry's environment, run:

```
poetry run python run.py
```

## Configuring secret_config.py
`secret_config.py` contains all of the secret API keys and things for your app.  It needs to be configured for a production release.

## Building CSS
Requires sassc

Run build_sass

## Running the production server
Set up the user account:
```
groupadd -r dreamingspires
useradd -r -g dreamingspires -d "/var/dreamingspires" -s "/bin/bash" dreamingspires
mkdir -p /var/dreamingspires
chown dreamingspires:dreamingspires /var/dreamingspires
```

Configure secret_config.py.

Set up ssh keys for users within the _DreamingSpires Servers_ GitHub team, and install them into `/var/dreamingspires/.ssh`, checking permissions.

Clone the repository into the `dreamingspires` user:
```
su dreamingspires
cd
git clone 
```

Copy up the systemd service from `dreamingspires-server/dreamingspires-server.service` to `/etc/systemd/system/dreamingspires-server.service`.

Install gunicorn
```
dnf install python3-gunicorn
```

Refresh systemctl and start server
```
systemctl daemon-reload
systemctl enable --now dreamingspires-server
```
