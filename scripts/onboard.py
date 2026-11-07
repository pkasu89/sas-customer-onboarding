import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


def check_customer(data):
    customer_id = data.get("customer_id", "")
    name = data.get("company_name", "")
    motto = data.get("motto", "")

    if not isinstance(customer_id, str) or not re.fullmatch(
        r"[a-z0-9][a-z0-9-]{0,38}[a-z0-9]", customer_id
    ):
        raise ValueError("Invalid customer ID")

    if not isinstance(name, str) or not 1 <= len(name) <= 100:
        raise ValueError("Invalid company name")

    if not isinstance(motto, str) or not 1 <= len(motto) <= 160:
        raise ValueError("Invalid motto")

    if any(ord(ch) < 32 for ch in name + motto):
        raise ValueError("Invalid characters in company details")

    return customer_id, name, motto

def onboard(file_name, dry_run=False):
    data = json.loads(Path(file_name).read_text(encoding="utf-8"))
    customer_id, name, motto = check_customer(data)

    namespace = "customer-" + customer_id
    release = "site-" + customer_id

    domain = os.getenv("CUSTOMER_DOMAIN_SUFFIX") or "customers.example.com"

    if not re.fullmatch(r"[a-z0-9.-]+", domain):
        raise ValueError("Invalid domain")

    host = customer_id + "." + domain
    values = {
        "customer": {
            "id": customer_id,
            "name": name,
            "motto": motto
        },
        "ingress": {
            "host": host
        }
    }

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".json",
        delete=False
    ) as temp:
        json.dump(values, temp, ensure_ascii=False)
        values_file = temp.name

    command = [
        "helm", "upgrade", "--install", release, "charts/customer-site",
        "--namespace", namespace,
        "--create-namespace",
        "--wait",
        "--rollback-on-failure",
        "--timeout", "5m",
        "--values", values_file,
    ]

    try:
        if dry_run:
            print("Customer details look good.")
            print("Would deploy:", release, "in", namespace)
            return

        subprocess.run(command, check=True)
        print("Deployment done.")
        print("To view the website, run:")
        print(
            f"kubectl port-forward svc/{release}-nginx "
            f"8085:80 -n {namespace}"
        )
        print("Then open http://localhost:8085")

    finally:
        Path(values_file).unlink(missing_ok=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        onboard(args.file_name, args.dry_run)
    except (ValueError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print("Onboarding failed:", error)
        raise SystemExit(1)