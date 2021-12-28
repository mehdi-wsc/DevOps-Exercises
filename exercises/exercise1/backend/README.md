# Back-Test

## Installation


##### Python dependencies


    pip install -r requirement.txt


##### Configuration

Configuration is done through env variables. Can be done with a .env file locally

    
* For **SQlite** database, you need to setup those variables :
    - DB_TYPE="sqlite"
    - DB_NAME="db/database.db"
* For **Postgres** you need to setup those :
    - DB_TYPE="postgres"
    - DB_USER="POSTGRES USER NAME"
    - DB_PASSWORD="POSTGRES USER PASSWORKD"
    - DB_HOST="POSTGRES HOST"
    - DB_PORT=POSTGRES PORT
    - DB_NAME="DATABASE NAME"


##### Database


    SQLite : sqlite3 db/database.db '.read db/install.sql'

    Postgres : psql --host HOST -p PORT -d DB_NAME -U USER -W < db/install.postgres.sql 
    
    
Examples data


    SQLite : sqlite3 db/database.db '.read db/data.sql'

    Postgres : psql --host HOST -p PORT -d DB_NAME -U USER -W < db/data.postgres.sql 
    
    
## Run


    python app.py
    

## Routes

* Customers
    * list : `GET /customers`
    * from id : `GET /customers/:id`
    * create : `POST /customers`
        * [*Varchar*] first_name
        * [*Varchar*] last_name
        * [*Varchar*] email

* Drivers
    * list : `GET /drivers[?zone_id=:zone_id]`
    * from id : `GET /drivers/:id`
    * create : `POST /drivers`
        * [*Varchar*] first_name
        * [*Varchar*] last_name
        * [*Varchar*] email
        * [*Int*] zone_id

* Zones
    * list : `GET /zones`
    * from id : `GET /zones/:id`
    * check if position in zone : `GET /zone/geo/:lat_lng` (lat_lng = lat,lng)
    * create : `POST /zones`
        * [*Varchar*] name
        * [*Text*] polygon_json (must be an array of array [[lat, lng], ...])

* Products
    * list : `GET /products`
    * from id : `GET /products/:id`
    * create : `POST /products`
        * [*Varchar*] name
        * [*Float*] price_ht
    * add product price : `POST /products/:id/price`
        * [*Float*] price_ht

* Deliveries
    * list : `GET /deliveries[?customer_id=:customer_id][?driver_id=:driver_id][?zone_id=:zone_id][?date=:date]`
    * from id : `GET /deliveries/:id`
    * delivery vehicles : `GET /deliveries/:id/vehicles`
    * delivery products prices : `GET /deliveries/:id/products`
    * create : `POST /deliveries`
        * [*Int*] customer_id
        * [*Int*] driver_id
        * [*Varchar*] location
        * [*Datetime*] schedule_date
    * add vehicle to delivery : `POST /deliveries/:id/vehicle`
        * [*Float*] description
        * [*Int*] product_id (From products)
        * [*Float*] quantity

## Tests

Simple

    pytest -v

With coverage report:

    pytest -v --cov-config .coveragerc --cov --cov-report html
    
