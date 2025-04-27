COPY (
    SELECT
        ic.id,
        ic.certificate_number AS industrial_certificate_number
    FROM industrial_certificates ic
) TO 'your_path/madeinkz/datasets/industrial_certificates.csv' WITH CSV HEADER;
COPY (
    SELECT
        cat.id,
        cat.name AS category_certificate_name
    FROM category_certificates cat
) TO 'your_path/madeinkz/datasets/category_certificates.csv' WITH CSV HEADER;
COPY (
    SELECT
        cf.id,
        cf.name AS certificate_form_name
    FROM certificate_forms cf
) TO 'your_path/madeinkz/datasets/certificate_forms.csv' WITH CSV HEADER;
COPY (
    SELECT
        c.id,
        c.name AS country_name
    FROM countries c
) TO 'your_path/madeinkz/datasets/countries.csv' WITH CSV HEADER;
COPY (
    SELECT
        r.id,
        r.code,
        r.name AS rpp_name
    FROM rpp r
) TO 'your_path/madeinkz/datasets/rpp.csv' WITH CSV HEADER;
COPY (
    SELECT
        mf.bin_iin,
        mf.name AS manufacturer_name,
        mf.legal_address,
        mf.actual_address,
        mf.phone,
        mf.email,
        mf.website,
        mf.date_included_in_the_registry,
        mf.date_of_change,
        mf.number_of_employees,
        mf.oced_code,
        mf.kato,
        mf.production_capacity
    FROM manufacturers mf
) TO 'your_path/madeinkz/datasets/manufacturers.csv' WITH CSV HEADER;
COPY (
    SELECT
        p.id,
        p.name,
        p.tn_ved_eaes,
        p.kp_ved,
        p.unit_measurement,
        p.unit_code,
        p.quantity,
        p.dvc
    FROM products p
) TO 'your_path/madeinkz/datasets/products.csv' WITH CSV HEADER;
COPY (
    SELECT
        dc.document_id,
        dc.issue_date,
        dc.end_date,
        dc.authorisation_licence,
        mf.name AS manufacturer_name,
        mf.bin_iin
    FROM document_compliances dc
    LEFT JOIN manufacturers mf ON dc.manufacturer_bin_iin = mf.bin_iin
) TO 'your_path/madeinkz/datasets/document_compliances.csv' WITH CSV HEADER;
COPY (
    SELECT
        c.id,
        c.certificate_number,
        c.blank_number,
        c.issue_date,
        c.date_ending,
        c.purpose_receipt,
        c.origin_criterion,
        c.status,
        mf.name AS manufacturer_name,
        mf.bin_iin,
        p.name AS product_name,
        cf.name AS form_name,
        cat.name AS category_name,
        ic.certificate_number AS industrial_certificate_number,
        r.name AS rpp_name,
        exp_c.name AS export_country,
        imp_c.name AS import_country
    FROM certificates c
    LEFT JOIN manufacturers mf ON c.manufacturer_bin_iin = mf.bin_iin
    LEFT JOIN products p ON c.product_id = p.id
    LEFT JOIN certificate_forms cf ON c.form_id = cf.id
    LEFT JOIN category_certificates cat ON c.category_id = cat.id
    LEFT JOIN industrial_certificates ic ON c.industrial_certificate_id = ic.id
    LEFT JOIN rpp r ON c.rpp_id = r.id
    LEFT JOIN countries exp_c ON c.export_country_id = exp_c.id
    LEFT JOIN countries imp_c ON c.import_country_id = imp_c.id
) TO 'your_path/madeinkz/datasets/certificates.csv' WITH CSV HEADER;
COPY (
    SELECT
        c.id,
        c.certificate_number,
        cf.name AS form_name,
        cat.name AS category_name,
        m.name AS manufacturer_name,
        p.name AS product_name,
        ex.name AS export_country,
        im.name AS import_country,
        c.issue_date,
        c.date_ending,
        c.status
    FROM certificates c
    LEFT JOIN certificate_forms cf ON c.form_id = cf.id
    LEFT JOIN category_certificates cat ON c.category_id = cat.id
    LEFT JOIN manufacturers m ON c.manufacturer_bin_iin = m.bin_iin
    LEFT JOIN products p ON c.product_id = p.id
    LEFT JOIN countries ex ON c.export_country_id = ex.id
    LEFT JOIN countries im ON c.import_country_id = im.id
) TO 'your_path/madeinkz/datasets/certificates_full.csv' WITH CSV HEADER;








