# Postgres-Debezium-Mysql

The project replicate the tables of Postgres to Mysql using Debezium. 

## How to Run: 
```
export DEBEZIUM_VERSION=2.0

docker compose up -d --build
```

After running the project a FastAPI webserver is up to check the MySQL tables: 
```
http://localhost:8000/docs
```

## Structure: 

When the Postgres tables are created and MySql is ready the `Source Connector` is submitted so all the changes in the tables are captured and produced in their own topics.The topic format name is : `{prefix}.{public}.{tablename}` 
```
{
  "name": "shipment-source",  
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector", 
    "database.hostname": "postgres", 
    "database.port": "5432", 
    "database.user": "postgresuser", 
    "database.password": "postgrespw", 
    "database.dbname" : "shipment_db", 
    "database.server.name": "postgres", 
    "topic.prefix" : "pg",
    "table.whitelist": "public.shipments,public.orders",
    "slot.name" : "shipments"
  }
}
```



And then By submitting the `Jdbc Sink Connector`, the topics are consumed to do changes in Mysql(Creating tables, Insert/Update/Delete of rows).
```
{
    "name": "shipment-sink",
    "config": {
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "tasks.max": "1",
        "topics.regex": "pg\\.public\\.\\w+",
        "connection.url": "jdbc:mysql://mysql:3306/shipment_db",
        "connection.user": "shipments",
        "connection.password": "shippw",
        "transforms": "unwrap,route",
        "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
        "transforms.unwrap.drop.tombstones": "false",
        "transforms.route.replacement": "$3",
        "transforms.route.regex": "([^.]+)\\.([^.]+)\\.([^.]+)",
        "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
        "value.converter":"org.apache.kafka.connect.json.JsonConverter",
        "auto.create": "true",
        "insert.mode": "upsert",
        "delete.enabled": "true",
        "pk.mode": "record_key"
    }
}
```


## Additional Commands:

1. The Connectors are submitted in `read_api` container but if you want to do it manually you can use :
```
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @source.json

curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @sink.json
```


2. You can Check the connectors:
```
http://localhost:8083/connectors
```



3. Connect to Postgresql:
```
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB -c "select * from orders"'
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB -c "select * from shipments"'
```


4. Connect to Mysql: 
```
docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER  -p$MYSQL_PASSWORD shipment_db -e "select * from orders"'
docker-compose exec mysql bash -c 'mysql -u $MYSQL_USER  -p$MYSQL_PASSWORD shipment_db -e "select * from shipments"'
```


5. Add records to Postgres:
```
docker-compose exec postgres bash -c 'psql -U $POSTGRES_USER $POSTGRES_DB'
INSERT INTO public.orders (id, price, status, date_created) VALUES (6, 3000, 'Failed', '2022-10-19 00:17:00');
```