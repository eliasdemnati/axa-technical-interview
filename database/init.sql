CREATE SCHEMA IF NOT EXISTS public;

CREATE TYPE public.embark_location AS ENUM (
    'C',
    'Q',
    'S'
);

CREATE TYPE public.sex AS enum (
    'male',
    'female'
);

CREATE TABLE public.passengers (
    passenger_id        SERIAL PRIMARY KEY NOT NULL,
    p_class             INTEGER,
    name                VARCHAR,
    sex                 public.sex,
    age                 FLOAT,
    nb_sibling_spouse   INTEGER,
    nb_parent_children  INTEGER,
    ticket              VARCHAR,
    fare                FLOAT,
    cabin               VARCHAR,
    embark_location     public.embark_location
);

COPY passengers(passenger_id, p_class, name, sex, age, nb_sibling_spouse, nb_parent_children, ticket, fare, cabin, embark_location)
FROM '/docker-entrypoint-initdb.d/data.csv'
DELIMITER ','
CSV HEADER;
