
# Attendance Checking System

This project include classroom Checking and dormitory Checking systems.

Using Line Login Service to identify student and sync with their studentID. Each QR code generated for students can be accessed via Line Bot. 


## Installation

### Install Require Library
```bash
  pip install -r requirements.txt
```

### Sync Database
- Change the database to the one you want.
Or leave it if you use local database.  


- Run this command to make database schema    
```bash
  python manage.py makemigrations
  python manage.py migrate
```

### Run server
- For port 8000
```bash
  python manage.py runserver  
```
- For port another port
```bash
  python manage.py runserver {PORT}
```

### Create Line Login Channel
[Click Here to create!](https://developers.line.biz/console/channel/new?type=line-login)

- Go to section LIFF --> add LIFF App
- Copy Liff ID to paste to file 
  - static/js/student_app/login.js 
  - static/js/student_app/profile.js


### Create Line Message API (Line Bot)
[Click Here to create!](https://developers.line.biz/console/channel/new?type=messaging-api)

- Go to Tab Messaging API
  - Edit webhook url to "yourhost/bot/webhook/"
  - Click verify to confirm that it worked.

- Scroll Down to Channel Access Token
  - Click Issue and copy it
  - Paste it at  
    - bot_webhook/views.py  line 14

- Change Tab to Basic Setting
  - Copy channel secret
  - Paste it at the same file line 18