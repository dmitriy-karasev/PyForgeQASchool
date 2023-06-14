import requests
# import pytest
from faker import Faker

# automated tests for account POST endpoint
# in setup we create new account and then try to login with correct/incorrect credentials
# through this endpoint /api/AuthAccount/Login

BASE_URL = "http://restapi.adequateshop.com/api/"
ACCOUNT_ID = None

fake = Faker()

name = fake.name()
email = fake.email()
password = "123456"

print(f"Generated data for account creation are: name {name}, email {email}, password {password}")

json_for_account_creation = {
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
    create_account()

# def teardown_module(module):
#   delete_account()


def create_account():
    '''Account creation'''
    global ACCOUNT_ID
    request_url = BASE_URL + "AuthAccount/Registration"
    response = requests.post(request_url, json=json_for_account_creation)
    ACCOUNT_ID = response.json()["data"]["Id"]
    print(f"New account created with Id = {ACCOUNT_ID} in setup")

def test_empty_login_password():
    '''Tests correct response in case of empty strings for email and password'''
    request_url = BASE_URL + "AuthAccount/Login"
    response = requests.post(request_url, json=json_empty_credentials)
    print(f"Received response is {response.json()}")
    assert response.status_code == 400
    assert response.json()["Message"] == "The request is invalid."
    assert response.json()["ModelState"]["log.email"] == ["field is required"]
    assert response.json()["ModelState"]["log.password"] == ["field is required"]


def test_invalid_email():
    '''Tests correct response in case of invalid email'''
    request_url = BASE_URL + "AuthAccount/Login"
    response = requests.post(request_url, json=json_incorrect_email)
    print(f"Received response is {response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == "invalid username or password"


def test_invalid_password():
    '''Tests correct response in case of invalid password'''
    request_url = BASE_URL + "AuthAccount/Login"
    response = requests.post(request_url, json=json_incorrect_password)
    print(f"Received response is {response.json()}")
    assert response.status_code == 200
    assert response.json()["message"] == "invalid username or password"


def test_correct_login():
    '''Tests correct returned data on successful login'''
    request_url = BASE_URL + "AuthAccount/Login"
    response = requests.post(request_url, json=json_correct_email_and_password)
    print(f"Received response is {response.json()}")
    assert response.status_code == 200
    assert response.json()["code"] == 0
    assert response.json()["message"] == "success"
    assert response.json()["data"]["Id"] == ACCOUNT_ID
    assert response.json()["data"]["Name"] == name
    assert response.json()["data"]["Email"] == email

#
# def delete_account():
#     request_url = BASE_URL + f"CUSTOMER/{ACCOUNT_ID}"
#     response = requests.delete(request_url)
#     print("Customer deleted")
#     print(response.json())





