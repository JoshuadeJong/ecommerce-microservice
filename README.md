A small ecommerce website using three services.

### Frontend
A simple customer facing website created using Flask.  

When running, you can view this service on `localhost:5600`

### Catalog Microservice
A catalog service created using FastAPI and Elasticsearch. 

When running, you can view this service on `localhost:5601`

### Cart Microservice
A customer shopping cart service created used FastAPI and Redis.

When running, you can view this service on `localhost:5602`

## Docker
Build the entire project docker-compose files or build individual services using the docker-compose files.
`docker-compose build up`

## Know bugs

- An elasticsearch index must be created for the catalog service to work correctly. To create the index use the frontend or catalog service to create a new item in the inventory.
