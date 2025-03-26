CREATE TABLE certificate_forms (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE category_certificates (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  tn_ved_eaes VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(50),
  kp_ved VARCHAR(10),
  unit_measurement VARCHAR(50),
  unit_code VARCHAR(10),
  quantity INT
);

CREATE TABLE manufacturers (
  bin_iin VARCHAR(12) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  legal_address TEXT,
  actual_address TEXT,
  phone VARCHAR(20),
  email VARCHAR(100),
  website VARCHAR(100),
  date_included_in_the_registry DATE,
  date_of_change DATE,
  number_of_employees INT,
  oced_code VARCHAR(50),
  kato VARCHAR(50),
  production_capacity VARCHAR(100)
);

CREATE TABLE document_compliances (
  document_id VARCHAR(50) PRIMARY KEY,
  issue_date DATE,
  end_date DATE,
  authorisation_licence VARCHAR(50),
  manufacturer_bin_iin VARCHAR(12) NOT NULL,
  CONSTRAINT fk_document_compliances_manufacturer
    FOREIGN KEY (manufacturer_bin_iin)
    REFERENCES manufacturers(bin_iin)
);

CREATE TABLE rpp (
  rpp_code SERIAL PRIMARY KEY,
  rpp_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE industrial_certificates (
  id SERIAL PRIMARY KEY,
  certificate_number VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE countries (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE certificates (
  id SERIAL PRIMARY KEY,
  rpp_code INT NOT NULL,
  manufacturer_bin_iin VARCHAR(12) NOT NULL,
  product_id INT NOT NULL,
  form_id INT NOT NULL,
  category_id INT NOT NULL,
  industrial_certificate_id INT NOT NULL,
  certificate_number VARCHAR(50) UNIQUE NOT NULL,
  blank_number VARCHAR(50),
  issue_date DATE,
  purpose_receipt VARCHAR(255),
  origin_criterion VARCHAR(100),
  status VARCHAR(50),
  date_ending DATE,
  dvc VARCHAR(100),
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
