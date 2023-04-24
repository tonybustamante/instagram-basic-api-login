# instagram-basic-api-login
Python implementation of the instagram basic api login as outlined here: https://developers.facebook.com/docs/instagram-basic-display-api/getting-started


# Instructions

1. Export APP_ID and APP_SECRET environmental variables
2. Create config.ini file in the following format:
```
[urls]
CALLBACK_URI = https://somewebsite.com:5000/auth/callback
DASHBOARD_URI = https://somewebsite:5000/dashboard
```

3. Add the url above the the hostfile as follows:
```
127.0.0.1 somewebsite.com
```

4. run `flask run --cert=adhoc`
