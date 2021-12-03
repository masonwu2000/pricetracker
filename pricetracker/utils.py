"""
Contains utility functions regarding extracting information.
"""

import csv
import os
import glob
import smtplib
import ssl
import email.mime.text
import email.mime.multipart
import email.mime.application
import psycopg2
import logging

from pricetracker.pricetracker.constants import (
    TABLE_NAME,
    REGISTERED_USERS,
    PATH_TO_CSV_FILES,
    EMAIL,
    PASSWORD,
)
from pricetracker.pricetracker.db import config


def find_discount(product_name):
    """
    Check the product's discount between the past two days.

    :param product_name: (str) Name of the product to look up.
    :return: (int) Representing the percentage the product has been discounted. Returns -1 if an error occurs.
    """

    select_sql = (
        f"SELECT * FROM {TABLE_NAME} WHERE {TABLE_NAME}.product_name = {product_name} SORT BY "
        f"{TABLE_NAME}.scrape_date DESCENDING LIMIT 2"
    )

    params = config()

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as curs:
            curs.execute(select_sql)

        res = curs.fetchall()
        if len(res) < 2:
            logging.warning("Not enough rows for product to compare prices with.")
            return -1
        else:
            two_days_ago = res[1]
            one_day_ago = res[0]

            discount = (two_days_ago - one_day_ago) / two_days_ago
            return discount


def write_to_csv(filename, response):
    """
    Writes specific product information to a given csv file.

    :param filename: (str) Filename to write to.
    :param response: (TextResponse) Response object containing product information.
    :return: None
    """
    csv_file = csv.writer(open(filename, "a"))
    if os.stat(filename).st_size == 0:
        csv_file.writerow(["Product", "Price"])

    for product in response.css("div.ProductItem"):
        price_list = product.css("div.ProductItem__PriceList")
        price = price_list.css("span.ProductItem__Price::text").get()
        price = price.split(" ")[1]

        item_info = product.css("div.ProductItem__Info")
        item_title = item_info.css("h2.ProductItem__Title a::text").get()

        params = config()

        insert_sql = f"INSERT INTO {TABLE_NAME}(product_name, price) VALUES ({price}, {item_title})"
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as curs:
                curs.execute(insert_sql)

        csv_file.writerow([item_title, price, find_discount(item_title)])


def email_users():
    """
    Sends an email containing product information to all registered users.

    :return: None
    """
    msg = email.mime.multipart.MIMEMultipart()
    msg["Subject"] = "Product Info"
    msg["From"] = EMAIL
    body = email.mime.text.MIMEText(
        """Product information regarding Rawgear is attached."""
    )
    msg.attach(body)

    for csv_file in glob.glob(PATH_TO_CSV_FILES):
        file_object = open(csv_file, "rb")
        attachment = email.mime.application.MIMEApplication(
            file_object.read(), _subtype="csv"
        )
        attachment.add_header(
            "Content-Disposition", "attachment", filename=csv_file.split("/")[-1]
        )
        msg.attach(attachment)
        file_object.close()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL, PASSWORD)
        for user in REGISTERED_USERS:
            msg["TO"] = user
            server.sendmail(EMAIL, [user], msg.as_string())
