#Deployment:
1. you have put every depedencies in requirements.txt
2. init .gitignore to skip *.pyc  and some lib files
3. Install gunicorn
4. Install nginx
5. Configure to add gunicorn like a unit service in systemd:
  create a file in  `/etc/systemd/system/gunicorn.service` with content like this:
```
[Unit]
Description=gunicorn daemon
After=network.target
[Service]
User=huy.nv.ngo
Group=www-data
WorkingDirectory=/home/huy.nv.ngo/BookReview
ExecStart=/home/huy.nv.ngo/BookReview/bin/gunicorn --access-logfile /var/log/belt_reviewer/gunicorn-access.log --error-logfile /var/log/belt_reviewer/gunicorn-error.log --workers 3 --bind unix:/home/huy.nv.ngo/BookReview/belt_reviewer.sock belt_reviewer.wsgi:application
[Install]
WantedBy=multi-user.target
```
after that , first we have to use systemctl to reload all daemon
`sudo systemctl daemon-reload`
after we reload, start gunicorn daemon
`sudo systemctl start gunicorn`
after we start this daemon => enable it
`sudo systemctl enable gunicorn`

Tips: if we want to specific log for it use --access-logfile parameter and --error-logfile parameter

Please chmod for the log path before start gunicorn

So if you change any thing in service script => call `reload daemon`
So if you want to change source code in django => restart gunicorn to update this source code

6 Configure for nginx
create a new site_avaiable:
`vim /etc/nginx/sites-available/belt_reviewer`

```
server {
  listen 8000;
  server_name 0.0.0.0;
  location = /favicon.ico { access_log off; log_not_found off; }
  location /static/ {
      root /home/huy.nv.ngo/BookReview;
  }
  location / {
      include proxy_params;
      proxy_pass http://unix:/home/huy.nv.ngo/BookReview/belt_reviewer.sock;
  }
}
```
after that
`sudo ln -s /etc/nginx/sites-available/{{projectName}} /etc/nginx/sites-enabled`
`sudo nginx -t`

`sudo rm /etc/nginx/sites-enabled/default`
`sudo service nginx restart`


Tip to migrate data from Sqlite3 to mysql
```
Step to migrate data from sqlite3 to mysql
1.python manage.py dumpdata > datadump.json
2. Change settings.py to your mysql
3. Make sure you can connect on your mysql (permissions,etc)
4. python manage.py migrate --run-syncdb
5. Exclude contentype data with this snippet

from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()

6.python manage.py loaddata datadump.json
```