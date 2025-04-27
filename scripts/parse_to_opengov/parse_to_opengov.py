import os
from ckanapi import RemoteCKAN

CKAN_URL = "https://data.opengov.kz"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJZdWhCMXZuQU5DRDVXTGd6WjZOQmNLcXV0a2RIZVZYM21JQkRQbjMtZnMwIiwiaWF0IjoxNzQ1NDk5NDU4fQ.k3H5I-4L9TH7KKJFS1URtK59dioBnDtJ9_YEShCJfsI"
ORGANIZATION_ID = "origin-of-goods"

def create_dataset(remote_ckan, dataset_name, title, owner_org):
    dataset_descriptions = {
        "category_certificates": """
        Таблица содержит информацию о категориях сертификатов, выданных на продукцию.
        
        
        Более детальное описание значений из таблиц
        - id (integer): Уникальный идентификатор категории сертификата.
        - name (string): Название категории сертификата (например, "CT-KZ", "СТ-1").
        """,
        "certificate_forms": """
        Таблица содержит информацию о формах сертификатов, которые могут быть выданы для продукции.
        
        
        Более детальное описание значений из таблиц
        - id (integer): Уникальный идентификатор формы сертификата.
        - name (string): Название формы сертификата (например, "A", "EAV").
        """,
        "certificates": """
        Таблица содержит данные о сертификатах, подтверждающих происхождение товаров.
        
        
        Более детальное описание значений из таблиц
        - id (integer): Уникальный идентификатор сертификата.
        - rpp_id (integer): Ссылка на реестр производственных предприятий.
        - manufacturer_bin_iin (string): БИН/ИИН производителя.
        - product_id (integer): Идентификатор продукта.
        - form_id (integer): Идентификатор формы сертификата.
        - category_id (integer): Идентификатор категории сертификата.
        - industrial_certificate_id (integer): Идентификатор индустриального сертификата.
        - certificate_number (string): Номер сертификата о происхождении товара.
        - blank_number (string): Номер бланка сертификата.
        - issue_date (date): Дата выдачи сертификата.
        - purpose_receipt (string): Цель получения сертификата.
        - origin_criterion (string): Критерий происхождения товара (например, "P" — полностью произведен в РК).
        - status (string): Статус сертификата (например, "действителен", "аннулирован").
        - date_ending (date): Дата окончания действия сертификата.
        - export_country_id (integer): Идентификатор страны экспорта.
        - import_country_id (integer): Идентификатор страны импорта.
        """,
        "countries": """
        Таблица содержит информацию о странах, участвующих в международной торговле.
        
       
        Более детальное описание значений из таблиц
        - id (integer): Уникальный идентификатор страны.
        - name (string): Название страны.
        """,
        "document_compliances": """
        Таблица содержит данные о документах, подтверждающих соответствие продукции требованиям для получения сертификатов.
        
        
        Более детальное описание значений из таблиц
        - document_id (string): Уникальный идентификатор документа.
        - issue_date (date): Дата выдачи документа.
        - end_date (date): Дата окончания действия документа.
        - authorisation_licence (string): Номер и дата разрешения или лицензии.
        - manufacturer_bin_iin (string): БИН/ИИН производителя.
        """,
        "industrial_certificates": """
        Таблица содержит информацию о промышленной сертификации продукции.
        
        
        Более детальное описание значений из таблиц
        - id (integer): Уникальный идентификатор индустриального сертификата.
        - certificate_number (string): Номер индустриального сертификата.
        """,
        "manufacturers": """
        Таблица содержит информацию о производителях, зарегистрированных в реестре.
        
        
        Более детальное описание значений из таблиц
        - bin_iin (string): БИН/ИИН производителя.
        - name (string): Название производителя.
        - legal_address (string): Юридический адрес производителя.
        - actual_address (string): Фактический адрес производителя.
        - phone (string): Контактный телефон.
        - email (string): Адрес электронной почты.
        - website (string): Веб-сайт производителя.
        - date_included_in_the_registry (date): Дата включения в реестр.
        - date_of_change (date): Дата последнего изменения данных.
        - number_of_employees (integer): Количество сотрудников.
        - oced_code (string): Код по Общему классификатору видов экономической деятельности.
        - kato (string): Код по классификатору административно-территориальных объектов.
        - production_capacity (string): Производственная мощность.
        """,
        "products": """
        Таблица содержит информацию о продукции, для которой были получены сертификаты происхождения.
        
        
        Более детальное описание значений из таблиц
        - id (integer): Уникальный идентификатор продукта.
        - tn_ved_eaes (string): Код товара по Товарной номенклатуре внешнеэкономической деятельности ЕАЭС.
        - name (string): Наименование продукта.
        - kp_ved (string): Код по классификатору продукции по видам экономической деятельности.
        - unit_measurement (string): Единица измерения.
        - unit_code (string): Код единицы измерения.
        - quantity (integer): Количество продукции.
        - dvc (string): Дополнительные характеристики продукции.
        """,
        "rpp": """
        Таблица содержит информацию о реестре производственных предприятий, зарегистрированных в системе.
        
        
        Более детальное описание значений из таблиц
        - id (integer): Уникальный идентификатор записи в реестре производственных предприятий.
        - code (string): Код предприятия.
        - name (string): Наименование предприятия.
        """
    }

    title_mapping = {
        "category_certificates": "Категории сертификатов происхождении товаров",
        "certificate_forms": "Формы сертификатов происхождении товаров",
        "certificates": "Сертификаты происхождении товаров",
        "countries": "Страны происхождении товаров",
        "document_compliances": "Документы о соответствии продукции происхождении товаров",
        "industrial_certificates": "Индустриальные сертификаты происхождении товаров",
        "manufacturers": "Производители происхождении товаров",
        "products": "Продукция происхождении товаров",
        "rpp": "Реестр производственных предприятий происхождении товаров"
    }

    description = dataset_descriptions.get(dataset_name, "")
    title = title_mapping.get(dataset_name, dataset_name)  # Используем читаемое название

    dataset_dict = {
    "name": dataset_name,
    "title": title,
    "owner_org": owner_org,
    "notes": description,
    "author": "Jeleubay Aslan",
    "author_email": "Aslan.dzheleubaj.04@gmail.com",  
    "url": "https://atameken.kz/ru/services/56-reestr-sertifikatov-o-proishozhdenii-tovara",
    "tags": [{"name": "сертификаты"}, {"name": "товары"}]
}

    return remote_ckan.action.package_create(**dataset_dict)


def upload_resource(remote_ckan, package_id_or_name, filepath, resource_name):
    resource_dict = {
        "package_id": package_id_or_name,
        "name": resource_name,
        "format": "CSV",
        "upload": open(filepath, "rb"),
    }
    return remote_ckan.action.resource_create(**resource_dict)


def main():
    ckan = RemoteCKAN(CKAN_URL, apikey=API_KEY)
    files = [
        "datasets/category_certificates.csv",
        "datasets/certificate_forms.csv",
        "datasets/certificates.csv",
        "datasets/countries.csv",
        "datasets/document_compliances.csv",
        "datasets/industrial_certificates.csv",
        "datasets/manufacturers.csv",
        "datasets/products.csv",
        "datasets/rpp.csv",
    ]

    for file in files:
        filepath = file
        filename = os.path.basename(filepath)
        base_name, ext = os.path.splitext(filename)

        dataset_name = base_name
        title = base_name

        try:
            created_dataset = create_dataset(ckan, dataset_name, title, ORGANIZATION_ID)
            print(f"Набор данных создан: {created_dataset.get('name')}")
        except Exception as e:
            print(f"Ошибка при создании набора данных: {e}")
            continue

        resource_name = filename

        try:
            created_resource = upload_resource(ckan, dataset_name, filepath, resource_name)
            print(f"Ресурс создан, ID ресурса: {created_resource.get('id')}")
        except Exception as e:
            print(f"Ошибка при загрузке ресурса: {e}")
            continue


if __name__ == "__main__":
    main()
