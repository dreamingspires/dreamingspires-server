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
