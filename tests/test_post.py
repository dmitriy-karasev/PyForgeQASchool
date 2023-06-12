import requests
# import pytest
from faker import Faker

# TODO - move json into helper

BASE_URL = "http://restapi.adequateshop.com/api/"
CUSTOMER_ID = None

fake = Faker()

name = fake.name()
email = fake.email()
password = "123456"

print(f"Generated data are: name {name}, email {email}, password {password}")

json_for_customer_creation = {
    "name": name,
    "email": email,
    "password": password
      }

json_empty_credentials = {
    "email": "",
    "password": ""
      }

json_incorrect_email = {
    "email": email + "test",
    "password": password
      }

json_incorrect_password = {
    "email": email,
    "password": password*2
      }

json_correct_email_and_password = {
    "email": email,
    "password": password
      }


def setup_module(module):
    create_customer()

# def teardown_module(module):
#     delete_customer()

# @pytest.fixture(autouse=True)
# def setup_and_teardown():
#     create_customer()
#     yield
#     delete_customer()


def create_customer():
    global CUSTOMER_ID
    request_url = BASE_URL + "AuthAccount/Registration"
    print("Entering setup")
    print(json_for_customer_creation)
    response = requests.post(request_url, json=json_for_customer_creation)
    print(response.json())
    CUSTOMER_ID = response.json()["data"]["Id"]
    print(f"Customer created in setup before tests with Id = {CUSTOMER_ID}")


def test_empty_login_password():
    request_url = BASE_URL + "AuthAccount/Login"
    print(json_empty_credentials)
    response = requests.post(request_url, json=json_empty_credentials)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["Message"] == "The request is invalid."
    assert response.json()["ModelState"]["log.email"] == ["field is required"]
    assert response.json()["ModelState"]["log.password"] == ["field is required"]


def test_invalid_email():
    request_url = BASE_URL + "AuthAccount/Login"
    print(json_incorrect_email)
    response = requests.post(request_url, json=json_incorrect_email)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "invalid username or password"


def test_invalid_password():
    request_url = BASE_URL + "AuthAccount/Login"
    print(json_incorrect_password)
    response = requests.post(request_url, json=json_incorrect_password)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "invalid username or password"


def test_correct_login():
    request_url = BASE_URL + "AuthAccount/Login"
    print(json_correct_email_and_password)
    response = requests.post(request_url, json=json_correct_email_and_password)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["message"] == "success"
    assert response.json()["data"]["Id"] == CUSTOMER_ID
    assert response.json()["data"]["Name"] == name
    assert response.json()["data"]["Email"] == email


def delete_customer():
    request_url = BASE_URL + f"CUSTOMER/{CUSTOMER_ID}"
    response = requests.delete(request_url)
    print("Customer deleted")
    print(response.json())


def delete_tourist(id):
    request_url = BASE_URL + f"Tourist/{id}"
    response = requests.delete(request_url)
    print("Customer deleted")
    print(response.json())
