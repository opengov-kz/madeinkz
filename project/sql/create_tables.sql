CREATE TABLE certificate_forms (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE category_certificates (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  tn_ved_eaes VARCHAR(500) UNIQUE NOT NULL,
  name TEXT,
  kp_ved VARCHAR(500),
  unit_measurement VARCHAR(500),
  unit_code VARCHAR(500),
  quantity INT
);

CREATE TABLE manufacturers (
  bin_iin VARCHAR(12) PRIMARY KEY,
  name VARCHAR(1000) NOT NULL,
  legal_address TEXT,
  actual_address TEXT,
  phone TEXT,
  email VARCHAR(1000),
  website VARCHAR(1000),
  date_included_in_the_registry DATE,
  date_of_change DATE,
  number_of_employees INT,
  oced_code VARCHAR(1000),
  kato VARCHAR(1000),
  production_capacity VARCHAR(1000)
);

CREATE TABLE document_compliances (
  document_id TEXT PRIMARY KEY,
  issue_date DATE,
  end_date DATE,
  authorisation_licence TEXT,
  manufacturer_bin_iin VARCHAR(12) NOT NULL,
  CONSTRAINT fk_document_compliances_manufacturer
    FOREIGN KEY (manufacturer_bin_iin)
    REFERENCES manufacturers(bin_iin)
);

CREATE TABLE rpp (
  rpp_code SERIAL PRIMARY KEY,
  rpp_name TEXT UNIQUE NOT NULL
);

CREATE TABLE industrial_certificates (
  id SERIAL PRIMARY KEY,
  certificate_number VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE countries (
  id SERIAL PRIMARY KEY,
  name VARCHAR(500) UNIQUE NOT NULL
);

CREATE TABLE certificates (
  id SERIAL PRIMARY KEY,
  rpp_code INT NOT NULL,
  manufacturer_bin_iin VARCHAR(12) NOT NULL,
  product_id INT NOT NULL,
  form_id INT NOT NULL,
  category_id INT NOT NULL,
  industrial_certificate_id INT NOT NULL,
  certificate_number VARCHAR(500) UNIQUE NOT NULL,
  blank_number VARCHAR(1000),
  issue_date DATE,
  purpose_receipt TEXT,
  origin_criterion TEXT,
  status VARCHAR(500),
  date_ending DATE,
  dvc VARCHAR(500),
  export_country_id INT NOT NULL,
  import_country_id INT NOT NULL,
  CONSTRAINT fk_certificates_rpp FOREIGN KEY (rpp_code) REFERENCES rpp(rpp_code),
  CONSTRAINT fk_certificates_form FOREIGN KEY (form_id) REFERENCES certificate_forms(id),
  CONSTRAINT fk_certificates_category FOREIGN KEY (category_id) REFERENCES category_certificates(id),
  CONSTRAINT fk_certificates_manufacturer FOREIGN KEY (manufacturer_bin_iin) REFERENCES manufacturers(bin_iin),
  CONSTRAINT fk_certificates_product FOREIGN KEY (product_id) REFERENCES products(id),
  CONSTRAINT fk_certificates_industrial FOREIGN KEY (industrial_certificate_id) REFERENCES industrial_certificates(id),
  CONSTRAINT fk_certificates_export_country FOREIGN KEY (export_country_id) REFERENCES countries(id),
  CONSTRAINT fk_certificates_import_country FOREIGN KEY (import_country_id) REFERENCES countries(id)
);
