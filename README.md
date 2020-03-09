Authentication: 
```
    POST /auth/login {username: 'username', password: 'password'}
    POST /auth/logout 
    POST /auth/registration {username: 'username', password: 'password', email:'email@email.com'}
```

App endpoints:
```
   POST /generate-joke 
   GET /get-joke {id: id}
   GET /get-jokes-list 
   PUT /update-joke {id: id, joke: joke}
   POST /remove-joke {id: id}
```

Initial start:
```
   flask db init
   flask db migrate -m "First migration"
   flask db upgrade
```
