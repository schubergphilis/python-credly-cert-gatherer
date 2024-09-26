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


def load_users(users_file: str) -> list:
    users = []
    with open(users_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row.get("username")
            credly_username = row.get("credly_username")
            ms_transcript_id = row.get("ms_transcript_id")
            users.append(
                {
                    "username": username,
                    "credly_username": credly_username,
                    "ms_transcript_id": ms_transcript_id,
                }
            )
    return users


def fetch_user_badges(credly_username: str) -> list:
    badges = []
    url = f"https://www.credly.com/users/{credly_username}/badges.json"
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
                        "source": "Credly",
                    }
                )
    else:
        print(f"Failed to fetch badges for Credly username: {credly_username}")
    return badges


def fetch_ms_certifications(ms_transcript_id: str) -> list:
    certifications = []
    url = f"https://learn.microsoft.com/api/profiles/transcript/share/{ms_transcript_id}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        active_certs = data.get("certificationData", {}).get(
            "activeCertifications", []
        )
        for cert in active_certs:
            certification = {
                "badge_id": cert.get("certificationNumber"),
                "badge_name": cert.get("name"),
                "expires_at": cert.get("expiration"),
                "source": "Microsoft", 
            }
            certifications.append(certification)
    else:
        print(f"Failed to fetch MS certifications for transcript ID: {ms_transcript_id}")
    return certifications


def main():
    certs_file = "certs.csv"
    users_file = "users.csv"
    certs = load_certs(certs_file)
    users = load_users(users_file)

    matched_certs = []
    expiring_certs = []
    cert_summary = {}

    for user in users:
        username = user.get("username")
        credly_username = user.get("credly_username")
        ms_transcript_id = user.get("ms_transcript_id")
        print(
            f"Processing user: Username={username}, Credly Username={credly_username}, MS Transcript ID={ms_transcript_id}"
        )
        user_badges = []
        if credly_username:
            credly_badges = fetch_user_badges(credly_username)
            filtered_badges = []
            for badge in credly_badges:
                if badge["badge_id"] in certs or badge["badge_name"] in certs.values():
                    filtered_badges.append(badge)
            user_badges.extend(filtered_badges)
        if ms_transcript_id:
            ms_certs = fetch_ms_certifications(ms_transcript_id)
            user_badges.extend(ms_certs)
        user_matched_badges = []
        for badge in user_badges:
            matched_cert = {
                "username": username,
                "badge_id": badge["badge_id"],
                "badge_name": badge["badge_name"],
                "expires_at": badge["expires_at"],
                "source": badge["source"],  
            }
            user_matched_badges.append(matched_cert)
            if badge["expires_at"]:
                expiring_certs.append(matched_cert)
            # Update cert_summary with source
            cert_key = (badge["badge_name"], badge["source"])
            cert_summary[cert_key] = cert_summary.get(cert_key, 0) + 1
        matched_certs.extend(user_matched_badges)

    with open(
        "output/summary_report.csv", "w", newline="", encoding="utf-8"
    ) as csvfile:
        fieldnames = ["badge_name", "source", "cert_count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for (cert_name, source), count in cert_summary.items():
            writer.writerow(
                {"badge_name": cert_name, "source": source, "cert_count": count}
            )

    with open(
        "output/detailed_report.csv", "w", newline="", encoding="utf-8"
    ) as csvfile:
        fieldnames = ["username", "badge_id", "badge_name", "expires_at", "source"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for cert in matched_certs:
            writer.writerow(cert)

    print("Reports generated successfully.")


if __name__ == "__main__":
    main()
