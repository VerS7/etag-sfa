"""
Simple script for adding mock data to app API
"""

import os
import time
from random import choice, randint
from os import getenv

import requests
from dotenv import load_dotenv

from fakegen.loader import load_all
from fakegen.generator import ProductBuilder


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

data_files = os.path.join(os.path.dirname(__file__), "fakegen/categories")
api_url = f"{getenv('API_URL')}:{getenv('API_PORT')}/api/product/{getenv('API_TOKEN')}"

random_barcodes = [str(randint(111_111_111, 999_999_999)) for _ in range(150)]

builder = ProductBuilder(
    data=load_all(data_files),
    barcode_generator=lambda: choice(random_barcodes),
    price_multiplier=1.3,
    sale_chance=0.4,
    sale_multiplier=0.2,
)

with requests.Session() as session:
    while True:
        try:
            product = list(builder.generate_completed_product())[0]
            print(f"POST | {str(product)[:70]}... | ", end="")

            response = requests.post(
                api_url, data=product.model_dump_json().encode("utf-8")
            )

            if response.status_code == 401:
                print("FAIL! 401 Unauthorised!")
                continue

            print("SUCCESS!")
            time.sleep(0.2)

        except requests.exceptions.ConnectionError:
            print("FAIL!\n")
            exit()

        except KeyboardInterrupt:
            exit()

        except Exception as e:
            print(f"Uncaught error! {e}")
            exit()
