import yaml
import requests
import logging
from bs4 import BeautifulSoup
import csv

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

PLATFORM_NAME_CREDLY = "CREDLY"


def get_value_of_html_tag(url: str, div_class: str):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        heading = soup.find(class_=div_class)

        if heading:
            return heading.get_text(strip=True)
        else:
            return "Heading not found."
    else:
        return f"Failed to fetch the page. Status code: {response.status_code}"


def get_credly_badges_of(url: str, source: str, per_page: int = 48):
    page = 1
    items = []
    has_more_pages = True

    while has_more_pages:
        paginated_url = f"{url}.json?page={page}&per={per_page}"
        try:
            data = requests.get(paginated_url).json()
        except Exception as e:
            logging.error(f"Failed to fetch badges from {paginated_url}: {str(e)}")
            break

        if "data" in data and data["data"]:
            for item in data["data"]:
                cert_id = item.get("id")
                cert_name = item.get("name")
                if cert_id and cert_name:
                    items.append(
                        {
                            "cert_id": cert_id,
                            "cert_name": cert_name,
                            "source": source,
                            "platform": PLATFORM_NAME_CREDLY,
                        }
                    )
        else:
            logging.warning(
                f"{paginated_url} : Returned no badges or data might be missing"
            )
            break

        current_page = data["metadata"]["current_page"]
        total_pages = data["metadata"]["total_pages"]

        if current_page < total_pages:
            page += 1
        else:
            has_more_pages = False

    return items


def get_certs() -> list:
    certs = []

    config_file = "credly.yml"
    with open(config_file, "r") as file:
        config_data = yaml.safe_load(file)
    if config_data["whitelist"]:
        for whitelist in config_data["whitelist"]:
            if not whitelist.get("cert_name") or not whitelist.get("cert_id"):
                logging.warning(
                    "Whitelist is invalid please check cert_name or cert_id is missing"
                )
                continue
            whitelist["source"] = "whitelist"
            whitelist["platform"] = PLATFORM_NAME_CREDLY
            certs.append(whitelist)

    if config_data["collections"]:
        for collection in config_data["collections"]:
            collection_badges = get_credly_badges_of(
                collection,
                "Collection: "
                + get_value_of_html_tag(collection, "ac-heading ac-heading--subhead"),
            )
            certs.extend(collection_badges)

    if config_data["organizations"]:
        for organization in config_data["organizations"]:
            organization_badges = get_credly_badges_of(
                organization,
                "Organization: "
                + get_value_of_html_tag(
                    organization,
                    "ac-heading ac-heading--badge-name-hero organization_header__title ac-heading--serif-primary-large",
                ),
            )
            certs.extend(organization_badges)

    if config_data["blacklist"]:
        blacklist_ids = {
            blacklist.get("cert_id") for blacklist in config_data["blacklist"]
        }
        blacklist_names = {
            blacklist.get("cert_name") for blacklist in config_data["blacklist"]
        }

        filtered_certs = [
            cert
            for cert in certs
            if cert.get("cert_id") not in blacklist_ids
            and cert.get("cert_name") not in blacklist_names
        ]
        certs = filtered_certs
    return certs


def generate_csv(certs: dict):
    csv_file = "certificates.csv"
    csv_headers = ["cert_id", "cert_name", "source", "platform"]

    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(certs)

    print(f"Certificates written to {csv_file}")


if __name__ == "__main__":
    certs = get_certs()

    generate_csv(certs)
