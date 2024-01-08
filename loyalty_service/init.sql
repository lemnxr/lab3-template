--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

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
-- Name: loyaltys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.loyaltys (
    id integer NOT NULL,
    username character varying(80) NOT NULL,
    reservation_count integer NOT NULL,
    status character varying(80) NOT NULL,
    discount integer NOT NULL
);


ALTER TABLE public.loyaltys OWNER TO postgres;

--
-- Name: loyaltys_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.loyaltys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.loyaltys_id_seq OWNER TO postgres;

--
-- Name: loyaltys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.loyaltys_id_seq OWNED BY public.loyaltys.id;


--
-- Name: loyaltys id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loyaltys ALTER COLUMN id SET DEFAULT nextval('public.loyaltys_id_seq'::regclass);


--
-- Data for Name: loyaltys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.loyaltys (id, username, reservation_count, status, discount) FROM stdin;
\.

INSERT INTO public.loyaltys (id, username, reservation_count, status, discount)
VALUES
    (1,'Test Max',25,'GOLD',10);


--
-- Name: loyaltys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.loyaltys_id_seq', 2, false);


--
-- Name: loyaltys loyaltys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loyaltys
    ADD CONSTRAINT loyaltys_pkey PRIMARY KEY (id);


--
-- Name: loyaltys loyaltys_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.loyaltys
    ADD CONSTRAINT loyaltys_username_key UNIQUE (username);


--
-- Name: ix_loyaltys_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_loyaltys_id ON public.loyaltys USING btree (id);


--
-- PostgreSQL database dump complete
--