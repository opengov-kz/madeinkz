BEGIN;

CREATE TABLE IF NOT EXISTS category_certificates
(
    id serial NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT category_certificates_pkey PRIMARY KEY (id),
    CONSTRAINT category_certificates_name_key UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS certificate_forms
(
    id serial NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT certificate_forms_pkey PRIMARY KEY (id),
    CONSTRAINT certificate_forms_name_key UNIQUE (name)
);


CREATE TABLE IF NOT EXISTS certificates
(
    id serial NOT NULL,
    rpp_id integer,
    manufacturer_bin_iin text COLLATE pg_catalog."default",
    product_id integer,
    form_id integer,
    category_id integer,
    industrial_certificate_id integer,
    certificate_number character varying(3000) COLLATE pg_catalog."default" ,
    blank_number character varying(3000) COLLATE pg_catalog."default",
    issue_date date,
    purpose_receipt text COLLATE pg_catalog."default",
    origin_criterion text COLLATE pg_catalog."default",
    status character varying(3000) COLLATE pg_catalog."default",
    date_ending date,
    export_country_id integer,
    import_country_id integer,
    CONSTRAINT certificates_pkey PRIMARY KEY (id),
    CONSTRAINT certificates_certificate_number_key UNIQUE (certificate_number)
);

CREATE TABLE IF NOT EXISTS countries
(
    id serial NOT NULL,
    name character varying(3000) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT countries_pkey PRIMARY KEY (id),
    CONSTRAINT countries_name_key UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS document_compliances
(
    document_id text COLLATE pg_catalog."default" NOT NULL,
    issue_date date,
    end_date date,
    authorisation_licence text COLLATE pg_catalog."default",
    manufacturer_bin_iin text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT document_compliances_pkey PRIMARY KEY (document_id)
);

CREATE TABLE IF NOT EXISTS industrial_certificates
(
    id serial NOT NULL,
    certificate_number character varying(3000) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT industrial_certificates_pkey PRIMARY KEY (id),
    CONSTRAINT industrial_certificates_certificate_number_key UNIQUE (certificate_number)
);

CREATE TABLE IF NOT EXISTS manufacturers
(
    bin_iin text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    legal_address text COLLATE pg_catalog."default",
    actual_address text COLLATE pg_catalog."default",
    phone text COLLATE pg_catalog."default",
    email character varying(3000) COLLATE pg_catalog."default",
    website character varying(3000) COLLATE pg_catalog."default",
    date_included_in_the_registry date,
    date_of_change date,
    number_of_employees integer,
    oced_code character varying(3000) COLLATE pg_catalog."default",
    kato character varying(3000) COLLATE pg_catalog."default",
    production_capacity character varying(3000) COLLATE pg_catalog."default",
    CONSTRAINT manufacturers_pkey PRIMARY KEY (bin_iin)
);

CREATE TABLE IF NOT EXISTS products
(
    id serial NOT NULL,
    tn_ved_eaes character varying(3000) COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default",
    kp_ved character varying(3000) COLLATE pg_catalog."default",
    unit_measurement character varying(3000) COLLATE pg_catalog."default",
    unit_code character varying(3000) COLLATE pg_catalog."default",
    quantity bigint,
    dvc character varying(3000) COLLATE pg_catalog."default",  -- Добавлено поле dvc
    CONSTRAINT products_pkey PRIMARY KEY (id)
);

CREATE UNIQUE INDEX unique_product ON products (tn_ved_eaes, md5(name));

CREATE TABLE IF NOT EXISTS rpp
(
    id serial NOT NULL,
    code character varying(3000) COLLATE pg_catalog."default",
    name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT rpp_pkey PRIMARY KEY (id),
    CONSTRAINT rpp_code_key UNIQUE (code),
    CONSTRAINT rpp_name_key UNIQUE (name)
);

ALTER TABLE IF EXISTS certificates
    ADD CONSTRAINT certificates_category_id_fkey FOREIGN KEY (category_id)
    REFERENCES category_certificates (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL;

ALTER TABLE IF EXISTS certificates
    ADD CONSTRAINT certificates_export_country_id_fkey FOREIGN KEY (export_country_id)
    REFERENCES countries (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS certificates
    ADD CONSTRAINT certificates_form_id_fkey FOREIGN KEY (form_id)
    REFERENCES certificate_forms (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS certificates
    ADD CONSTRAINT certificates_import_country_id_fkey FOREIGN KEY (import_country_id)
    REFERENCES countries (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS certificates
    ADD CONSTRAINT certificates_industrial_certificate_id_fkey FOREIGN KEY (industrial_certificate_id)
    REFERENCES industrial_certificates (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE IF EXISTS certificates
    ADD CONSTRAINT certificates_manufacturer_bin_iin_fkey FOREIGN KEY (manufacturer_bin_iin)
    REFERENCES manufacturers (bin_iin) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS certificates
    ADD CONSTRAINT certificates_product_id_fkey FOREIGN KEY (product_id)
    REFERENCES products (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS certificates
    ADD CONSTRAINT certificates_rpp_id_fkey FOREIGN KEY (rpp_id)
    REFERENCES rpp (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL;

ALTER TABLE IF EXISTS document_compliances
    ADD CONSTRAINT fk_document_compliances_manufacturer FOREIGN KEY (manufacturer_bin_iin)
    REFERENCES manufacturers (bin_iin) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;
