-- Table: Locations
CREATE TABLE locations (
	name varchar(255) PRIMARY KEY,
	latitude numeric(9,6) NOT NULL,
	longitude numeric(9,6) NOT NULL
);
-- Table: Subscribers
CREATE TABLE subscribers (
	id SERIAL PRIMARY KEY,
	username varchar(100) UNIQUE NOT NULL,
	password_hash varchar(255) NOT NULL,
	email varchar(255) UNIQUE NOT NULL,
	CONSTRAINT subscribers_location_fk FOREIGN KEY (location_name) REFERENCES locations(name)
);
-- Table: Weatherdata
CREATE TABLE weatherdata (
	id SERIAL PRIMARY KEY,
	location_name varchar(255) NOT NULL,
	time_to_flashover numeric(16,15),
	temperature numeric(4,2),
	humidity numeric(3,1),
	wind_speed numeric(3,1),
	timestamp timestamp NOT NULL,
	CONSTRAINT weatherdata_location_fk FOREIGN KEY (location_name) REFERENCES locations(name)
);


