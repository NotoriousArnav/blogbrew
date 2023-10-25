#!/usr/bin/env bash
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Restart Gunicorn
# systemctl restart gunicorn

# Configure Nginx (e.g., update the Nginx config file)
# cp /path/to/your/nginx/config /etc/nginx/sites-available/your-site
# ln -s /etc/nginx/sites-available/your-site /etc/nginx/sites-enabled/
# systemctl reload nginx

# Set up any other necessary services (e.g., background tasks, caching)

# Optionally, notify yourself or the team that the deployment is complete
echo "Deployment completed."