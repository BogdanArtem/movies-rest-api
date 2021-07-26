## Movies database
## Python3 Flask Elasticsearch Rest API

### To Setup and Start Development Enviroment
```bash
git clone https://github.com/BogdanArtem/movies-rest-api.git
cd movies-rest-api
docker-compose up
```

### Read Docs
http://0.0.0.0:5000/api/docs

### Users and permissions
username: Alex, password: 12345 (registered user)
username: Admin, password: 12345 (admin user)

### Get All Movies
```bash
curl -X GET http://0.0.0.0:5000/api/movies
```

### Get One Movie 
```bash
curl -X GET http://0.0.0.0:5000/api/movies/1
```

### Get Authentication token (registered users only)
```bash
curl -X POST -u Alex:12345 http://0.0.0.0:5000/api/tokens
```

### Add A New Movie (authorized users only)
```bash
curl -X POST http://0.0.0.0:5000/api/movies -H 'Content-Type: application/json' -H 'Authorization:Bearer place_for_your_token' -d '{"name": "Zombie-dinosaurs attack ", "director_id": 1, "date":"1978-01-01", "description": "A mythical artefact resurrected army of zombie-dinosaurs", "rating":3, "poster_url": "www.posters.com", "user_id": 1}'
```

### Edit An Existing Record (authorized users only)
```bash
curl -X PUT http://0.0.0.0:5000/api/movies/4 -H 'Content-Type: application/json' -H 'Authorization:Bearer place_for_your_token' -d '{"name": "Zombie-dinosaur epic attack"}'

```

### Sort Movies by rating
```bash
curl -X POST http://0.0.0.0:5000/api/movies/search -H 'Content-Type: application/json' -H 'Authorization:Bearer place_for_your_token' -d '{"sort": {"rating": "asc"}}'
```

### Sort Movies by date
```curl -X POST http://0.0.0.0:5000/api/movies/search -H 'Content-Type: application/json' -H 'Authorization:Bearer place_for_your_token' -d '{"sort": {"date": "desc"}}'
```

### Find Movies by partial match in all fielsd
```
curl -X POST http://0.0.0.0:5000/api/movies/search -H 'Content-Type: application/json' -H 'Authorization:Bearer place_for_your_token' -d '{"query: {"query_string": {"query": "sup*", "fields": ["*"]}}}'
```

### Find Movies by name full math
```
curl -X POST http://0.0.0.0:5000/api/movies/search -H 'Content-Type: application/json' -H 'Authorization:Bearer place_for_your_token' -d '{"query":{"multi_match": {"query": "Good", "fields": ["name"]}}}'
```

### Filter movies by date
```
curl -X POST http://0.0.0.0:5000/api/movies/search -H 'Content-Type: application/json' -H 'Authorization:Bearer place_for_your_token' -d '{"query": {
"range":{"date": {"from": "1995", "to": "2000"}}}}'
```

### Delete A Record (authorized users only)
```bash
curl -X DELETE http://0.0.0.0:5000/api/movies/4 -H 'Authorization:Bearer place_for_your_token'
```

### Test Output
```bash
$ pytest
tests/test_directors.py .....                                                                                                      [ 21%]
tests/test_genres.py .....                                                                                                         [ 43%]
tests/test_movies.py ........                                                                                                      [ 78%]
tests/test_users.py .....                                                                                                          [100%]

==================================================== 23 passed, 23 warnings in 49.31s ====================================================

```
