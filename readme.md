# Certification Badge Scraper and Report Generator

This project is designed to fetch certifications and badges for users from platforms like **Credly** and **Microsoft**, filter them based on provided configuration files (`azure.yml` and `credly.yml`), and generate detailed and summary reports in CSV format.

## Features

- Fetches certification data from **Credly** and **Microsoft Learn** using public APIs.
- Filters certifications based on a whitelist and blacklist defined in configuration files.
- Supports badge collection from **Credly** for specific organizations and collections.
- Generates two CSV reports:
  - `detailed_report.csv`: Detailed report of badges for each user.
  - `summary_report.csv`: Summary of badge counts by platform and source.

## Prerequisites

Make sure you have the following installed:

- **Python 3.12+**
- **pip** (Python package manager)

## Installation

1. Clone the repository:

2. Runs install and setup needed base scripts

   ```bash
   sh example.sh
   ```

3. (Optional) If you are in a development environment, install the additional development requirements:

   ```bash
   pip install -r dev-requirements.txt
   ```

## Configuration Files

The project uses two YAML configuration files for defining filtering rules:

### `azure.yml`

- Contains a whitelist and blacklist for Azure-specific certifications.
- Example:

  ```yaml
  # Add certifications that should be marked as Azure
  whitelist:
    - cert_id: 6ea45e81,
      cert_name: DOES NOT CONTAIN azure
  # Add certifications that should not be marked as Azure
  blacklist:
    - cert_id: FAKE_DOES_NOT_EXIST
      cert_name: FAKE_DOES_NOT_EXIST
  ```

### `credly.yml`

- Contains details of organizations and collections from **Credly**.
- Includes whitelist and blacklist for specific certifications.
- Example:

  ```yaml
  collections:
    - https://www.credly.com/organizations/amazon-web-services/collections/aws-certification-program-private-collection/badge_templates
  organizations:
    - https://www.credly.com/organizations/amazon-web-services/badges
  whitelist:
    - cert_id: 6069fb52-0c27-42d7-852b-6aa86ea45e81,
      cert_name: AWS Certified Cloud Practitioner
  blacklist:
    - cert_id: FAKE_DOES_NOT_EXIST
      cert_name: FAKE_DOES_NOT_EXIST
  ```

## Project Structure

```bash
.
├── azure.yml                # Azure-specific filtering rules
├── certificates.csv         # Fetched certifications (generated file)
├── credly.yml               # Credly-specific filtering rules
├── dev-requirements.txt      # Development requirements
├── example                  # Example users CSV
├── example.sh               # Example shell script for setup
├── get-cert-filter.py        # Fetches certifications based on config files
├── main.py                  # Main script to combine users and their certifications
├── output                   # Output folder for reports
│   ├── detailed_report.csv   # Detailed report (generated file)
│   └── summary_report.csv    # Summary report (generated file)
├── pyproject.toml            # Project configuration (optional)
├── readme.md                 # Project README
├── requirements.txt          # Python requirements
└── users.csv                 # List of users (username, Credly username, MS transcript ID)
```

## Usage

### Step 1: Add Users

Add the users you want to fetch certifications for in the `users.csv` file:

```csv
username,credly_username,ms_transcript_id
john_doe,john.credly,123456789
jane_doe,jane.credly,987654321
```

### Step 2: Run the Certification Fetcher

1. To fetch the certifications based on the YAML files (`credly.yml` and `azure.yml`), run the following script:

   ```bash
   python get-cert-filter.py
   ```

   This will generate the `certificates.csv` file with the filtered certification data.

### Step 3: Combine Users with Certifications

2. Run the main script to combine the fetched certifications with the users and generate the reports:

   ```bash
   python main.py
   ```

   This will create the following output files:

   - `output/detailed_report.csv`: Detailed list of certifications for each user.
   - `output/summary_report.csv`: Summary of certification counts by platform and source.

### Output Example

- **`detailed_report.csv`**:

  | username | badge_id  | badge_name                              | expires_at | source | platform  |
  | -------- | --------- | --------------------------------------- | ---------- | ------ | --------- |
  | john_doe | 123456789 | AWS Certified Cloud Practitioner        | 2024-12-31 | Credly | CREDLY    |
  | jane_doe | 987654321 | Microsoft Certified: Azure Fundamentals | 2025-01-15 | AZURE  | Microsoft |

- **`summary_report.csv`**:

  | badge_name                              | source | platform  | cert_count |
  | --------------------------------------- | ------ | --------- | ---------- |
  | AWS Certified Cloud Practitioner        | Credly | CREDLY    | 1          |
  | Microsoft Certified: Azure Fundamentals | AZURE  | Microsoft | 1          |
