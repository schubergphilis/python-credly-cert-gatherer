import csv

import requests


def load_certs(certs_file: str) -> dict:
    certs = {}
    with open(certs_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cert_id = row.get("cert_id")
            cert_name = row.get("cert_name")
            certs[cert_id] = cert_name
    return certs


def load_users(users_file: str) -> dict:
    users = []
    with open(users_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_name = row.get("user_name")
            users.append(user_name)
    return users


def fetch_user_badges(user_name: str) -> dict:
    badges = []
    url = f"https://www.credly.com/users/{user_name}/badges.json"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        badges_data = data.get("data")
        if badges_data:
            for badge in badges_data:
                badge_info = badge.get("badge_template")
                badge_name = badge_info.get("name")
                badge_id = badge.get("id")
                expires_at = badge.get("expires_at")
                badges.append(
                    {
                        "badge_id": badge_id,
                        "badge_name": badge_name,
                        "expires_at": expires_at,
                    }
                )
    else:
        print(f"Failed to fetch badges for user: {user_name}")
    return badges


def main():
    certs_file = "certs.csv"
    users_file = "users.csv"
    certs = load_certs(certs_file)
    users = load_users(users_file)

    matched_certs = []
    expiring_certs = []
    summary = {}

    for user in users:
        print(f"Processing user: {user}")
        user_badges = fetch_user_badges(user)
        user_matched_badges = []
        for badge in user_badges:
            if badge["badge_id"] in certs or badge["badge_name"] in certs.values():
                matched_cert = {
                    "user_name": user,
                    "badge_id": badge["badge_id"],
                    "badge_name": badge["badge_name"],
                    "expires_at": badge["expires_at"],
                }
                user_matched_badges.append(matched_cert)
                if badge["expires_at"]:
                    expiring_certs.append(matched_cert)
        matched_certs.extend(user_matched_badges)
        summary[user] = len(user_matched_badges)

    with open(
        "output/summary_report.csv", "w", newline="", encoding="utf-8"
    ) as csvfile:
        fieldnames = ["user_name", "cert_count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in summary.items():
            writer.writerow({"user_name": user, "cert_count": count})

    with open(
        "output/detailed_report.csv", "w", newline="", encoding="utf-8"
    ) as csvfile:
        fieldnames = ["user_name", "badge_id", "badge_name", "expires_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for cert in expiring_certs:
            writer.writerow(cert)

    print("Reports generated successfully.")


if __name__ == "__main__":
    main()
