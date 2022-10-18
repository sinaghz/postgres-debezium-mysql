# Postgres-Debezium-Mysql

The project replicate the tables of Postgres to Mysql using Debezium. 

## How to Run: 
```
export DEBEZIUM_VERSION=2.0

docker compose up -d --build

curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @source.json

curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @sink.json

```

You can Check the connectors:
``http://localhost:8083/connectors``

Connect to Postgresql:

```
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB -c "select * from orders"'
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB -c "select * from shipments"'
```

Connect to Mysql: 
```
docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER  -p$MYSQL_PASSWORD shipment_db -e "select * from orders"'
docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER  -p$MYSQL_PASSWORD shipment_db -e "select * from shipments"'
```

Add records to Postgres:
```
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB'
INSERT INTO public.orders (id, price, status, date_created) VALUES (6, 3000, 'Failed', '2022-10-19 00:17:00');
```