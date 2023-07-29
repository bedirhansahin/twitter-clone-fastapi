# TWITTER-API-CLONE

## This project is still in development!

### Technologies:
- FastAPI
- Pydantic
- PostgreSQL
- JWT
- Docker
- Docker-compose
- AWS EC2


**[Swagger Documentation](http://3.253.146.144/v1/docs)**


### Download the project locally:

- To download the project
```
git clone https://github.com/bedirhansahin/twitter-clone-fastapi.git
cd twitter-clone-fastapi
```

```
docker-compose up --build
```
- To create the schema
```
docker exec -it <postgres id> psql -U postgres
```
```
create schema if not exists twitter_clone
```
- To start the project
```
docker-compose up
```