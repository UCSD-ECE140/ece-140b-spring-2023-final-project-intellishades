# Usage:

To initialize database:
```
mysql -u <mysql_username> -p < init_db.sql
```

To start the server (in /code directory):
```
python server.py
```

# Change Log:

05/23/2023 Updated schedule code to send information to /update_schedule route, still need to get an IP for the raspberry pi and update the route. Possibly a template response?

05/01/2023 Modified file structure, now run everything in /code directory

04/24/2023 Created a basic login/logout functionality

04/24/2023 Initialized Database

04/24/2023 Initial Upload