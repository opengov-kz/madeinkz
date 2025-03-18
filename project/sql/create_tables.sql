CREATE TABLE RCC (
    rcc_code SERIAL PRIMARY KEY,
    rcc_name VARCHAR NOT NULL
);

CREATE TABLE ORIGIN_CERTIFICATES (
    certificate_number VARCHAR PRIMARY KEY,
    rcc_code INT REFERENCES RCC(rcc_code),
    form_number VARCHAR,
    issue_year INT,
    purpose VARCHAR,
    category VARCHAR,
    manufacturer_bin VARCHAR,
    manufacturer_name VARCHAR,
    manufacturer_address TEXT,
    issue_date DATE,
    expiry_date DATE,
    certificate_status VARCHAR,
    recipient_bin VARCHAR,
    recipient_name VARCHAR,
    recipient_address TEXT,
    certificate_form VARCHAR
);

CREATE TABLE HS_CODES (
    hs_code VARCHAR PRIMARY KEY,
    name VARCHAR
);

CREATE TABLE CP_VED_CODES (  
    cp_ved_code VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    notes TEXT
);

CREATE TABLE CERTIFICATE_PRODUCTS (
    id SERIAL PRIMARY KEY,
    certificate_number VARCHAR REFERENCES ORIGIN_CERTIFICATES(certificate_number),
    product_name VARCHAR,
    hs_code VARCHAR REFERENCES HS_CODES(hs_code),
    cp_ved_code VARCHAR REFERENCES CP_VED_CODES(cp_ved_code),  
    product_quantity DECIMAL,
    unit_of_measure VARCHAR,
    unit_code VARCHAR,
    origin_criterion VARCHAR,
    dvc VARCHAR
);

CREATE TABLE COUNTRIES (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR NOT NULL,
    country_code VARCHAR NOT NULL
);

CREATE TABLE CERTIFICATE_COUNTRIES (
    id SERIAL PRIMARY KEY,
    certificate_number VARCHAR REFERENCES ORIGIN_CERTIFICATES(certificate_number),
    origin_country_id INT REFERENCES COUNTRIES(country_id),
    recipient_country_id INT REFERENCES COUNTRIES(country_id)
);

CREATE TABLE INDUSTRIAL_CERTIFICATES (
    industrial_certificate_reg_number VARCHAR PRIMARY KEY,
    manufacturer_bin VARCHAR,
    manufacturer_name VARCHAR,
    okved_activity_type VARCHAR,
    kato_region VARCHAR,
    legal_address TEXT,
    postal_address TEXT,
    material_technical_base_address TEXT,
    phone VARCHAR,
    email VARCHAR,
    website VARCHAR,
    number_of_employees INT,
    registry_inclusion_date DATE,
    modification_date DATE,
    actualization_date DATE
);

CREATE TABLE INDUSTRIAL_CERTIFICATE_PRODUCTS (
    id SERIAL PRIMARY KEY,
    industrial_certificate_reg_number VARCHAR REFERENCES INDUSTRIAL_CERTIFICATES(industrial_certificate_reg_number),
    product_name VARCHAR,
    production_capacity DECIMAL,
    hs_code VARCHAR REFERENCES HS_CODES(hs_code),
    cp_ved_code VARCHAR REFERENCES CP_VED_CODES(cp_ved_code), 
    conformity_document_number VARCHAR,
    document_issue_date DATE,
    document_expiry_date DATE,
    license_number VARCHAR,
    license_date DATE
);
