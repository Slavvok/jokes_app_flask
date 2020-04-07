Authentication: 
```
   POST /auth/registration {username: 'username', password: 'password', email:'email@email.com'}
   POST /auth/jwt {username: 'username', password: 'password'} - get access_token
   POST /auth/logout 
```

App: ( Headers: {Authentication: "Bearer <access_token>"} )

```
   POST /generate-joke
   GET /get-joke/<id>
   GET /get-jokes-list
   POST /update-joke/<id>
   POST /remove-joke/<id>
```

Initial start:
```
   flask db init
   flask db migrate -m "First migration"
   flask db upgrade
```
