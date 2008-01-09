--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'Standard public schema';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: node; Type: TABLE; Schema: public; Owner: master; Tablespace:
--

CREATE TABLE node (
    id serial NOT NULL,
    name character varying(255)
);


ALTER TABLE public.node OWNER TO master;

--
-- Name: node_id_seq; Type: SEQUENCE SET; Schema: public; Owner: master
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('node', 'id'), 1, false);


--
-- Name: node_properties_log; Type: TABLE; Schema: public; Owner: master; Tablespace:
--

CREATE TABLE node_properties_log (
    id serial NOT NULL,
    node_id integer NOT NULL,
    property_id integer NOT NULL,
    "time" timestamp without time zone DEFAULT now() NOT NULL,
    value character varying(64),
    "comment" character varying(255)
);


ALTER TABLE public.node_properties_log OWNER TO master;

--
-- Name: node_properties; Type: VIEW; Schema: public; Owner: master
--

CREATE OR REPLACE VIEW node_properties AS
    SELECT npl.id, npl.node_id, npl.property_id, npl."time" AS last_change, npl.value, npl."comment" FROM node_properties_log npl, (SELECT node_properties_log.node_id, node_properties_log.property_id, max(node_properties_log."time") AS "time" FROM node_properties_log GROUP BY node_properties_log.node_id, node_properties_log.property_id) mr WHERE (((npl.node_id = mr.node_id) AND (npl.property_id = mr.property_id)) AND (npl."time" = mr."time"));


ALTER TABLE public.node_properties OWNER TO master;

--
-- Name: node_properties_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: master
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('node_properties_log', 'id'), 1, false);


--
-- Name: node_status_log; Type: TABLE; Schema: public; Owner: master; Tablespace:
--

CREATE TABLE node_status_log (
    id serial NOT NULL,
    node_id integer NOT NULL,
    status_id integer NOT NULL,
    "time" timestamp without time zone DEFAULT now() NOT NULL,
    "comment" character varying(64),
    user_id integer
);


ALTER TABLE public.node_status_log OWNER TO master;

--
-- Name: node_status; Type: VIEW; Schema: public; Owner: master
--

CREATE OR REPLACE VIEW node_status AS
    SELECT nsl.id, nsl.node_id, nsl.status_id, nsl."time" AS last_change, nsl."comment", nsl.user_id FROM node_status_log nsl, (SELECT node_status_log.node_id, max(node_status_log."time") AS "time" FROM node_status_log GROUP BY node_status_log.node_id) mr WHERE ((nsl.node_id = mr.node_id) AND (nsl."time" = mr."time"));


ALTER TABLE public.node_status OWNER TO master;

--
-- Name: node_status_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: master
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('node_status_log', 'id'), 1, false);


--
-- Name: property; Type: TABLE; Schema: public; Owner: master; Tablespace:
--

CREATE TABLE property (
    id serial NOT NULL,
    name character varying(32),
    description character varying(255)
);


ALTER TABLE public.property OWNER TO master;

--
-- Name: property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: master
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('property', 'id'), 1, false);


--
-- Name: status; Type: TABLE; Schema: public; Owner: master; Tablespace:
--

CREATE TABLE status (
    id serial NOT NULL,
    name character varying(32),
    description character varying(255)
);


ALTER TABLE public.status OWNER TO master;

--
-- Name: status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: master
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('status', 'id'), 1, false);


--
-- Name: users; Type: TABLE; Schema: public; Owner: master; Tablespace:
--

CREATE TABLE users (
    id serial NOT NULL,
    username character varying(32),
    name character varying(64)
);


ALTER TABLE public.users OWNER TO master;

--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: master
--

SELECT pg_catalog.setval(pg_catalog.pg_get_serial_sequence('users', 'id'), 1, false);


--
-- Data for Name: node; Type: TABLE DATA; Schema: public; Owner: master
--

COPY node (id, name) FROM stdin;
\.


--
-- Data for Name: node_properties_log; Type: TABLE DATA; Schema: public; Owner: master
--

COPY node_properties_log (id, node_id, property_id, "time", value, "comment") FROM stdin;
\.


--
-- Data for Name: node_status_log; Type: TABLE DATA; Schema: public; Owner: master
--

COPY node_status_log (id, node_id, status_id, "time", "comment", user_id) FROM stdin;
\.


--
-- Data for Name: property; Type: TABLE DATA; Schema: public; Owner: master
--

COPY property (id, name, description) FROM stdin;
\.


--
-- Data for Name: status; Type: TABLE DATA; Schema: public; Owner: master
--

COPY status (id, name, description) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: master
--

COPY users (id, username, name) FROM stdin;
\.


--
-- Name: node_name_key; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY node
    ADD CONSTRAINT node_name_key UNIQUE (name);


--
-- Name: node_pkey; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY node
    ADD CONSTRAINT node_pkey PRIMARY KEY (id);


--
-- Name: node_properties_log_pkey; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY node_properties_log
    ADD CONSTRAINT node_properties_log_pkey PRIMARY KEY (id);


--
-- Name: node_status_log_pkey; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY node_status_log
    ADD CONSTRAINT node_status_log_pkey PRIMARY KEY (id);


--
-- Name: property_name_key; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY property
    ADD CONSTRAINT property_name_key UNIQUE (name);


--
-- Name: property_pkey; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY property
    ADD CONSTRAINT property_pkey PRIMARY KEY (id);


--
-- Name: status_name_key; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY status
    ADD CONSTRAINT status_name_key UNIQUE (name);


--
-- Name: status_pkey; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: master; Tablespace:
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: node_properties_log_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: master
--

ALTER TABLE ONLY node_properties_log
    ADD CONSTRAINT node_properties_log_node_id_fkey FOREIGN KEY (node_id) REFERENCES node(id);


--
-- Name: node_properties_log_property_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: master
--

ALTER TABLE ONLY node_properties_log
    ADD CONSTRAINT node_properties_log_property_id_fkey FOREIGN KEY (property_id) REFERENCES property(id);


--
-- Name: node_status_log_node_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: master
--

ALTER TABLE ONLY node_status_log
    ADD CONSTRAINT node_status_log_node_id_fkey FOREIGN KEY (node_id) REFERENCES node(id);


--
-- Name: node_status_log_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: master
--

ALTER TABLE ONLY node_status_log
    ADD CONSTRAINT node_status_log_status_id_fkey FOREIGN KEY (status_id) REFERENCES status(id);


--
-- Name: node_status_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: master
--

ALTER TABLE ONLY node_status_log
    ADD CONSTRAINT node_status_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

