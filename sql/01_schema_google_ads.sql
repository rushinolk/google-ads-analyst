CREATE TABLE IF NOT EXISTS dim_location (
	id_location  SERIAL PRIMARY KEY,
	name_location TEXT UNIQUE NOT null
);

CREATE TABLE IF NOT EXISTS dim_keyword 		(
	id_keyword SERIAL PRIMARY KEY,
	keyword TEXT UNIQUE NOT null
);

CREATE TABLE IF NOT EXISTS dim_campaign_name (
	id_campaign_name SERIAL PRIMARY KEY,
	campaign_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_device  (
	id_device SERIAL PRIMARY KEY,
	device TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS fct_anuncio (
	id_anuncio VARCHAR(10) NOT NuLL PRIMARY KEY,
	id_campaign_name INT REFERENCES dim_campaign_name(id_campaign_name),
	id_location INT REFERENCES dim_location(id_location),
	id_device INT REFERENCES dim_device(id_device),
	id_keyword INT REFERENCES dim_keyword(id_keyword),
	clicks INT,
	impressions INT,
	cost FLOAT,
	leads INT,
	conversions INT,
	sale_amount FLOAT,
	ad_date DATE
);


