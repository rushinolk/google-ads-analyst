CREATE TABLE dim_location IF NOT EXISTS(
	id_location int not null PRIMARY KEY,
	name_location UNIQUE NOT null
)

CREATE TABLE dim_keyword IF NOT EXISTS(
	id_keyword int not null PRIMARY KEY,
	keyword UNIQUE NOT null
)

CREATE TABLE dim_campaign_name IF NOT EXISTS (
	id_campaign_name INT NOT NULL PRIMARY KEY,
	campaign_name UNIQUE NOT NULL
)

CREATE TABLE dim_device IF NOT EXISTS (
	id_device INT NOT NULL PRIMARY KEY,
	device UNIQUE NOT NULL
)

CREATE TABLE fct_anuncio IF NOT EXISTS(
	id_anuncio VARCHAR(10) NOT NuLL PRIMARY KEY,
	id_campaign_name INT FOREIGN KEY,
	id_location INT FOREIGN KEY,
	id_device INT FOREIGN KEY,
	id_keyword INT FOREIGN KEY,
	clicks INT,
	impressons INT,
	cost FLOAT,
	leads int,
	conversons int
	sale_amount FLOAT,
	ad_date datetime'
)