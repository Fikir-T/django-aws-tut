#!/bin/bash
# Log everything output by this script to a file for troubleshooting
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

echo "================ STARTING DJANGO DEPLOYMENT ================"

# 1. Update OS and install dependencies
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv python3-dev libpq-dev postgresql-client nginx git

# 2. Clone your Django Project
cd /home/ubuntu
# If the directory already exists from previous attempts, delete it first to avoid conflicts
sudo rm -rf django-app
git clone https://github.com/Fikir-T/django-aws-tut.git django-app
cd /home/ubuntu/django-app

# 3. Set up Python Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create local environment variables (.env)
cat <<'EOF' > .env
DJANGO_SECRET_KEY=django-insecure-ukv+n*33s^p54#3vm9+gw(5me#*yj+3e#x+2kb6k@2pi4%dx)m
DJANGO_DEBUG=False
DB_HOST=django-postgres-db.cdwyqmq4o0qb.eu-north-1.rds.amazonaws.com
DB_NAME=appdb
DB_USER=postgres
DB_PASSWORD=88638863
DB_PORT=5432
USE_AWS_S3=True
AWS_STORAGE_BUCKET_NAME=django-aws-tut
AWS_S3_REGION_NAME=eu-north-1
EOF

# Safely load the env variables into the system environment
set -a
source .env
set +a

# 5. Run Django migrations and collect static files to S3
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# 6. Configure Gunicorn Systemd Service
cat <<EOF | sudo tee /etc/systemd/system/gunicorn.service
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/django-app
EnvironmentFile=/home/ubuntu/django-app/.env
ExecStart=/home/ubuntu/django-app/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          DjangoBase.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Start and enable Gunicorn
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 7. Configure Nginx as a Reverse Proxy
cat <<EOF | sudo tee /etc/nginx/sites-available/django
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

# Enable Nginx configuration and restart services
sudo ln -sf /etc/nginx/sites-available/django /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx
sudo systemctl enable nginx

echo "================ DJANGO DEPLOYMENT COMPLETE ================"