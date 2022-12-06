--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

-- Started on 2022-11-27 20:55:32

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
-- TOC entry 209 (class 1259 OID 32819)
-- Name: vacunas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vacunas (
    nombre name NOT NULL,
    apellido name NOT NULL,
    cedula numeric(10,0) NOT NULL,
    correo text NOT NULL,
    nacimiento date,
    domicilio text,
    telefono numeric(10,0),
    numvacunas numeric NOT NULL
);


ALTER TABLE public.vacunas OWNER TO postgres;

--
-- TOC entry 3166 (class 2606 OID 32825)
-- Name: vacunas vacunas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vacunas
    ADD CONSTRAINT vacunas_pkey PRIMARY KEY (cedula);


--
-- TOC entry 3311 (class 0 OID 0)
-- Dependencies: 209
-- Name: TABLE vacunas; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.vacunas TO employeuser;


-- Completed on 2022-11-27 20:55:32

--
-- PostgreSQL database dump complete
--

