# README

## Overview

This project consists of two Python scripts:

- `main.py`: Processes user badges from Credly and generates summary and detailed reports in CSV format.
- `fetch.py`: Fetches certificate information from Credly and outputs certificate IDs and names.

An `example.sh` script is also provided to copy example configuration files.

## Prerequisites

- Python 3.12 or higher
- `pip` package installer

## Setup

### 1. Clone the Repository

Clone this repository to your local machine:

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

#### On Unix or MacOS:

```bash
python3 -m venv venv
```

#### On Windows:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### On Unix or MacOS:

```bash
source venv/bin/activate
```

#### On Windows:

```bash
venv\Scripts\activate
```

### 4. Install Requirements

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Prepare Configuration Files

Ensure you have the following CSV files in your project directory:

- `certs.csv`: Contains certificate IDs and names.
- `users.csv`: Contains usernames of Credly users.

If you don't have these files, you can use the `example.sh` script to copy example configurations:

```bash
bash example.sh
```

### 2. Fetch Certificates

Use the `fetch.py` script to fetch certificate information from Credly.

```bash
python fetch.py
```

When prompted, enter the URL of the Credly badge templates JSON. For example:

```
Url of group including json: https://www.credly.com/organizations/amazon-web-services/collections/aws-certification-program-private-collection/badge_templates.json
```

The script will output certificate IDs and names, which you can save to `certs.csv`.

### 3. Run the Main Script

Execute `main.py` to process user badges and generate reports:

```bash
python main.py
```

The script will:

- Load certificates from `certs.csv`.
- Load users from `users.csv`.
- Fetch badges for each user from Credly.
- Match badges with the certificates.
- Generate two reports:
  - `output/summary_report.csv`: Summary of certificates per user.
  - `output/detailed_report.csv`: Detailed report of expiring certificates.

### 4. View the Reports

The generated reports are saved in the `output` directory:

- `summary_report.csv`
- `detailed_report.csv`

You can open these CSV files with any spreadsheet application or text editor.

## Output

After running `Main.py`, you should see:

```
Processing user: user1
Processing user: user2
...
Reports generated successfully.
```

## Notes

- Ensure your `certs.csv` and `users.csv` files are correctly formatted.
- The scripts rely on the Credly API, so an active internet connection is required.
- If you encounter any issues, check the console output for error messages.
