-- Key tables

CREATE TABLE node (
    id serial NOT NULL PRIMARY KEY,
    name character varying(255) UNIQUE
);

CREATE TABLE property (
    id serial NOT NULL PRIMARY KEY,
    name character varying(64) UNIQUE,
    description character varying(255)
);

CREATE TABLE status (
    id serial NOT NULL PRIMARY KEY,
    name character varying(32) UNIQUE,
    description character varying(255)
);

CREATE TABLE event (
    id SERIAL PRIMARY KEY,
    name CHARACTER VARYING(32) UNIQUE,
    description CHARACTER VARYING(255)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username character varying(32),
    name character varying(64)
);


-- Log Tables

CREATE TABLE node_properties_log (
    id serial NOT NULL PRIMARY KEY,
    node_id integer NOT NULL REFERENCES node(id),
    property_id integer NOT NULL REFERENCES property(id),
    "time" timestamp without time zone DEFAULT now() NOT NULL,
    value character varying(64),
    "comment" character varying(255)
);


CREATE TABLE node_status_log (
    id serial NOT NULL PRIMARY KEY,
    node_id integer NOT NULL REFERENCES node(id),
    status_id integer NOT NULL REFERENCES status(id),
    "time" timestamp without time zone DEFAULT now() NOT NULL,
    "comment" character varying(64),
    user_id integer NOT NULL REFERENCES users(id)
);

CREATE TABLE node_event_log (
    id SERIAL PRIMARY KEY,
    node_id INTEGER NOT NULL REFERENCES node(id),
    event_id INTEGER NOT NULL REFERENCES event(id),
    "time" TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    "comment" TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id)
);


-- View Definitions

CREATE OR REPLACE VIEW node_properties AS
    SELECT npl.id, npl.node_id, npl.property_id, npl."time" AS last_change, npl.value, npl."comment" FROM node_properties_log npl, (SELECT node_properties_log.node_id, node_properties_log.property_id, max(node_properties_log."time") AS "time" FROM node_properties_log GROUP BY node_properties_log.node_id, node_properties_log.property_id) mr WHERE (((npl.node_id = mr.node_id) AND (npl.property_id = mr.property_id)) AND (npl."time" = mr."time"));

CREATE OR REPLACE VIEW node_status_view AS
 SELECT distinct on(nsl.node_id) nsl.id, nsl.node_id, nsl.status_id, nsl."time" AS last_change, nsl.comment, nsl.user_id
   FROM 
    node_status_log nsl, 
    ( SELECT node_status_log.node_id, max(node_status_log."time") AS "time" FROM node_status_log GROUP BY node_status_log.node_id) mr
  WHERE nsl.node_id = mr.node_id AND nsl."time" = mr."time";

-- Materialized Views

CREATE TABLE node_status (
    id serial NOT NULL,
    node_id integer NOT NULL PRIMARY KEY REFERENCES node(id),
    status_id integer NOT NULL REFERENCES status(id),
    last_change timestamp without time zone DEFAULT now() NOT NULL,
    "comment" character varying(64),
    user_id integer NOT NULL REFERENCES users(id)
);

CREATE OR REPLACE LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION node_status_log_insert_tf()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM node_status WHERE node_id = NEW.node_id;
    INSERT INTO node_status
        (id, node_id, status_id, last_change, comment, user_id)
        VALUES
        (NEW.*);
    RETURN NULL;
END;
$$
LANGUAGE plpgsql;
CREATE TRIGGER node_status_log_after_insert_t AFTER INSERT ON node_status_log FOR EACH ROW EXECUTE PROCEDURE node_status_log_insert_tf();
