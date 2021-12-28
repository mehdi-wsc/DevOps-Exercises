CREATE TABLE customers(
	id Serial PRIMARY KEY,
	first_name Varchar(64) NOT NULL,
	last_name Varchar(64) NOT NULL,
	email Varchar(64) NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE zones(
	id Serial PRIMARY KEY,
	name Varchar(64) NOT NULL,
	polygon Text NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drivers(
	id Serial PRIMARY KEY,
	first_name Varchar(64) NOT NULL,
	last_name Varchar(64) NOT NULL,
	email Varchar(64) NOT NULL,
	zone_id Integer NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (zone_id) REFERENCES zones (id) 
 	ON DELETE SET NULL ON UPDATE NO ACTION
);

CREATE TABLE products(
	id Serial PRIMARY KEY,
	name Varchar(256) NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products_prices(
	id Serial PRIMARY KEY, 
	product_id Integer NOT NULL,
	price_ht Real NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (product_id) REFERENCES products (id)
	ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE deliveries(
	id Serial PRIMARY KEY,
	customer_id Integer NOT NULL,
	driver_id Integer NOT NULL,
	zone_id Integer NOT NULL,
	location Varchar(256) NOT NULL,
	lat Real NOT NULL,
	lng Real NOT NULL,
	schedule_date timestamp NOT NULL,
	start_delivery_date timestamp NULL,
	end_delivery_date timestamp NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (customer_id) REFERENCES customers (id)
	ON DELETE RESTRICT ON UPDATE NO ACTION,
	FOREIGN KEY (driver_id) REFERENCES drivers (id)
	ON DELETE RESTRICT ON UPDATE NO ACTION,
	FOREIGN KEY (zone_id) REFERENCES zones (id)
	ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE deliveries_products(
	id Serial PRIMARY KEY,
	delivery_id Integer NOT NULL,
	product_id Integer NOT NULL,
	name Varchar(256) NOT NULL,
	price_ht Real NOT NULL,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (delivery_id) REFERENCES deliveries (id)
	ON DELETE CASCADE ON UPDATE NO ACTION,
	FOREIGN KEY (product_id) REFERENCES products (id)
	ON DELETE RESTRICT ON UPDATE NO ACTION
);

CREATE TABLE deliveries_vehicles(
	id Serial PRIMARY KEY, 
	delivery_id Integer NOT NULL,
	product_id Integer NOT NULL,
	description Varchar(256) NOT NULL,
	quantity Real DEFAULT 0.0,
	created_at timestamp DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (delivery_id) REFERENCES deliveries (id)
	ON DELETE CASCADE ON UPDATE NO ACTION,
	FOREIGN KEY (product_id) REFERENCES deliveries_products (id)
	ON DELETE RESTRICT ON UPDATE NO ACTION
);

