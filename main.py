import subprocess

from pricetracker.utils import email_users

if __name__ == "__main__":
    subprocess.check_output(["python3", "run_crawlers.py"])
    email_users()
