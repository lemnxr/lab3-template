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
-- Name: hotels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hotels (
    id integer NOT NULL,
    hotel_uid uuid NOT NULL,
    name character varying(255) NOT NULL,
    country character varying(80) NOT NULL,
    city character varying(80) NOT NULL,
    address character varying(255) NOT NULL,
    stars integer,
    price integer NOT NULL
);


ALTER TABLE public.hotels OWNER TO postgres;

--
-- Name: hotels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hotels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hotels_id_seq OWNER TO postgres;

--
-- Name: hotels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hotels_id_seq OWNED BY public.hotels.id;


--
-- Name: reservation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reservation (
    id integer NOT NULL,
    reservation_uid uuid NOT NULL,
    username character varying(80) NOT NULL,
    payment_uid uuid NOT NULL,
    hotel_id integer,
    status character varying(20) NOT NULL,
    start_date date,
    end_date date
);


ALTER TABLE public.reservation OWNER TO postgres;

--
-- Name: reservation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reservation_id_seq OWNER TO postgres;

--
-- Name: reservation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reservation_id_seq OWNED BY public.reservation.id;


--
-- Name: hotels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hotels ALTER COLUMN id SET DEFAULT nextval('public.hotels_id_seq'::regclass);


--
-- Name: reservation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation ALTER COLUMN id SET DEFAULT nextval('public.reservation_id_seq'::regclass);


--
-- Data for Name: hotels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.hotels (id, hotel_uid, name, country, city, address, stars, price) FROM stdin;
\.

INSERT INTO public.hotels (id, hotel_uid, name, country, city, address, stars, price)
VALUES
    (1,'049161bb-badd-4fa8-9d90-87c9a82b0668','Ararat Park Hyatt Moscow','Россия','Москва','Неглинная ул., 4',5,10000);

--
-- Data for Name: reservation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reservation (id, reservation_uid, username, payment_uid, hotel_id, status, start_date, end_date) FROM stdin;
\.


--
-- Name: hotels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.hotels_id_seq', 1, false);


--
-- Name: reservation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reservation_id_seq', 1, false);


--
-- Name: hotels hotels_hotel_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hotels
    ADD CONSTRAINT hotels_hotel_uid_key UNIQUE (hotel_uid);


--
-- Name: hotels hotels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hotels
    ADD CONSTRAINT hotels_pkey PRIMARY KEY (id);


--
-- Name: reservation reservation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_pkey PRIMARY KEY (id);


--
-- Name: reservation reservation_reservation_uid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_reservation_uid_key UNIQUE (reservation_uid);


--
-- Name: ix_hotels_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_hotels_id ON public.hotels USING btree (id);


--
-- Name: ix_reservation_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reservation_id ON public.reservation USING btree (id);


--
-- Name: reservation reservation_hotel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reservation
    ADD CONSTRAINT reservation_hotel_id_fkey FOREIGN KEY (hotel_id) REFERENCES public.hotels(id);


--
-- PostgreSQL database dump complete
--