--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

-- Started on 2020-04-12 18:08:01

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 277 (class 1255 OID 59031)
-- Name: AuxilioMesDelete(); Type: FUNCTION; Schema: public; Owner: -
--
-- Table: public.feedback

-- DROP TABLE public.feedback;
-- Table: public.curso
CREATE TABLE public.curso (
    id serial PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Table: public.edicao
CREATE TABLE public.edicao (
    id serial PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Table: public.edicao_curso
CREATE TABLE public.edicao_curso (
    id serial PRIMARY KEY,
    edicao_id INTEGER REFERENCES public.edicao(id) ON DELETE CASCADE,
    curso_id INTEGER REFERENCES public.curso(id) ON DELETE CASCADE,
    vagas_ac INTEGER DEFAULT 0,
    vagas_ppi_br INTEGER DEFAULT 0,
    vagas_publica_br INTEGER DEFAULT 0,
    vagas_ppi_publica INTEGER DEFAULT 0,
    vagas_publica INTEGER DEFAULT 0,
    vagas_deficientes INTEGER DEFAULT 0
);

-- Table: public.candidato
CREATE TABLE public.candidato (
    id serial PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    curso_id INTEGER REFERENCES public.curso(id) ON DELETE CASCADE,
    nota FLOAT NOT NULL
);


