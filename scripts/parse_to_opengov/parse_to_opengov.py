import os
from ckanapi import RemoteCKAN
import argparse
from dotenv import load_dotenv

load_dotenv()


def create_dataset(remote_ckan, dataset_name, title, owner_org):
    dataset_descriptions = {
        "dataset1": """
        Реестр выданных сертификатов о происхождении товара формы «CT-KZ» для внутреннего обращения на территории Республики Казахстан. Содержит информацию о номере сертификата, дате выдачи, заявителе, наименовании товара и регионе.
        """,
        "dataset2": """
        Реестр содержит данные о выданных сертификатах формы «СТ-1», подтверждающих происхождение товаров, экспортируемых в страны СНГ. Включает сведения о дате выдачи, заявителе, наименовании продукции и регионе.
        """,
        "dataset3": """
        Реестр включает информацию о сертификатах происхождения формы «CT-2», предназначенных для экспорта товаров в страны, с которыми у Республики Казахстан заключены преференциальные соглашения. Указаны основные сведения о товаре, компании-заявителе и регионе.
        """,
        "dataset4": """
        Данный реестр содержит сведения о сертификатах формы «СТ-3», используемых при экспорте товаров в определённые зарубежные государства. Включает информацию о дате, получателе, производителе и продукции.
        """,
        "dataset5": """
        Реестр охватывает сертификаты формы «EAV», оформляемые при экспорте в рамках Евразийского экономического союза (ЕАЭС). Представлены данные о продукции, экспортёре и параметрах поставки.
        """,
        "dataset6": """
        Реестр содержит сведения о сертификатах формы «A», выдаваемых в рамках Генеральной системы преференций (GSP) при экспорте товаров в развитые страны. Указаны данные о производителе, товаре и условиях поставки.
        """,
        "dataset7": """
        Содержит данные о сертификатах происхождения формы «Оригинал», подтверждающих происхождение товаров при поставке в страны, не охваченные преференциальными соглашениями. Включены сведения о компании, товаре и регионе.
        """,
        "dataset8": """
        Реестр предприятий, получивших индустриальные сертификаты, подтверждающие статус отечественного производителя товаров, работ или услуг. Содержит информацию о производителях, типах продукции и регионах деятельности.
        """
    }

    title_mapping = {
        "dataset1": "Реестр выданных сертификатов о происхождении товара формы «CT-KZ» (для внутреннего обращения)",
        "dataset2": "Реестр выданных сертификатов о происхождении товара формы «СТ-1» (для экспорта)",
        "dataset3": "Реестр выданных сертификатов о происхождении товара формы «CT-2» (для экспорта)",
        "dataset4": "Реестр выданных сертификатов о происхождении товара формы «СТ-3» (для экспорта)",
        "dataset5": "Реестр выданных сертификатов о происхождении товара формы «EAV» (для экспорта)",
        "dataset6": "Реестр выданных сертификатов о происхождении товара формы «A» (для экспорта)",
        "dataset7": "Реестр выданных сертификатов о происхождении товара формы «Оригинал» (для экспорта)",
        "dataset8": "Реестр отечественных производителей товаров, работ, услуг (Индустриальный сертификат)",
    }

    description = dataset_descriptions.get(dataset_name, "")
    title = title_mapping.get(dataset_name, dataset_name)  

    dataset_dict = {
    "name": dataset_name,
    "title": title,
    "owner_org": owner_org,
    "notes": description,  
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
    parser = argparse.ArgumentParser(description="Upload datasets to CKAN portal.")
    parser.add_argument("--ckan-url")
    parser.add_argument("--api-key")
    parser.add_argument("--org-id")

    args = parser.parse_args()

    ckan_url = args.ckan_url or os.getenv("CKAN_URL")
    api_key = args.api_key or os.getenv("API_KEY")
    organization_id = args.org_id or os.getenv("ORGANIZATION_ID")

    if not all([ckan_url, api_key, organization_id]):
        print("❌ Ошибка: Не все параметры заданы. Убедитесь, что они переданы через аргументы или присутствуют в .env.")
        return

    ckan = RemoteCKAN(ckan_url, apikey=api_key)

    files = [
        "datasets/dataset1.csv",
        "datasets/dataset2.csv",
        "datasets/dataset3.csv",
        "datasets/dataset4.csv",
        "datasets/dataset5.csv",
        "datasets/dataset6.csv",
        "datasets/dataset7.csv",
        "datasets/dataset8.csv",
    ]

    for filepath in files:
        filename = os.path.basename(filepath)
        base_name, _ = os.path.splitext(filename)
        dataset_name = base_name

        try:
            created_dataset = create_dataset(ckan, dataset_name, dataset_name, organization_id)
            print(f"✅ Набор данных создан: {created_dataset.get('name')}")
        except Exception as e:
            print(f"❌ Ошибка при создании набора данных: {e}")
            continue

        try:
            created_resource = upload_resource(ckan, dataset_name, filepath, filename)
            print(f"✅ Ресурс загружен: {created_resource.get('id')}")
        except Exception as e:
            print(f"❌ Ошибка при загрузке ресурса: {e}")
            continue


if __name__ == "__main__":
    main()