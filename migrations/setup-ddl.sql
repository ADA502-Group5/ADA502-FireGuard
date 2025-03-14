CREATE TABLE public.registrations (
	id int8 NOT NULL,
	contact_details varchar(1000) NOT NULL,
	location_name varchar(1000) NOT NULL,
	CONSTRAINT registrations_pk PRIMARY KEY (id)
);
