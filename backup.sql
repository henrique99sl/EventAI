--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: eventos_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO eventos_user;

--
-- Name: events; Type: TABLE; Schema: public; Owner: eventos_user
--

CREATE TABLE public.events (
    id integer NOT NULL,
    name character varying NOT NULL,
    date date NOT NULL,
    venue_id integer NOT NULL,
    owner_id integer NOT NULL
);


ALTER TABLE public.events OWNER TO eventos_user;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: eventos_user
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO eventos_user;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eventos_user
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: eventos_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying NOT NULL,
    role character varying(20)
);


ALTER TABLE public.users OWNER TO eventos_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: eventos_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO eventos_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eventos_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: venues; Type: TABLE; Schema: public; Owner: eventos_user
--

CREATE TABLE public.venues (
    id integer NOT NULL,
    name character varying NOT NULL,
    address character varying
);


ALTER TABLE public.venues OWNER TO eventos_user;

--
-- Name: venues_id_seq; Type: SEQUENCE; Schema: public; Owner: eventos_user
--

CREATE SEQUENCE public.venues_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.venues_id_seq OWNER TO eventos_user;

--
-- Name: venues_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: eventos_user
--

ALTER SEQUENCE public.venues_id_seq OWNED BY public.venues.id;


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: venues id; Type: DEFAULT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.venues ALTER COLUMN id SET DEFAULT nextval('public.venues_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: eventos_user
--

COPY public.alembic_version (version_num) FROM stdin;
0bc15a8e839b
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: eventos_user
--

COPY public.events (id, name, date, venue_id, owner_id) FROM stdin;
1	Evento de Teste	2025-10-01	1	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: eventos_user
--

COPY public.users (id, username, email, password_hash, role) FROM stdin;
1	admin	admin@email.com	hash	admin
\.


--
-- Data for Name: venues; Type: TABLE DATA; Schema: public; Owner: eventos_user
--

COPY public.venues (id, name, address) FROM stdin;
1	Auditório Central	Av. Principal, 1000
\.


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eventos_user
--

SELECT pg_catalog.setval('public.events_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eventos_user
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: venues_id_seq; Type: SEQUENCE SET; Schema: public; Owner: eventos_user
--

SELECT pg_catalog.setval('public.venues_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: venues venues_pkey; Type: CONSTRAINT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.venues
    ADD CONSTRAINT venues_pkey PRIMARY KEY (id);


--
-- Name: events events_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venues(id);


--
-- Name: events fk_owner_id; Type: FK CONSTRAINT; Schema: public; Owner: eventos_user
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT fk_owner_id FOREIGN KEY (owner_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

