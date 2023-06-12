import requests
# import pytest
from faker import Faker
from datetime import datetime

# TODO - move json into helper

BASE_URL = "http://restapi.adequateshop.com/api/"
ACCOUNT_ID = None
TOURIST_ID = None

fake = Faker()

name = fake.name()
email = fake.email()
password = "123456"

tourist_name = fake.name()
tourist_email = fake.email()
tourist_created_date = datetime.utcnow().isoformat().replace("+00:00", "Z")
tourist_location = "Earth"

print(f"Generated data for account creation are: name {name}, email {email}, password {password}")
print(f"Generated data for tourist creation are: name {tourist_name}, email {tourist_email}, \
      tourist_location {tourist_location}, created time {tourist_created_date}")

json_for_tourist_creation = {
  "id": 0,
  "tourist_name": tourist_name,
  "tourist_email": tourist_email,
  "tourist_location": tourist_location,
  "createdat": tourist_created_date
}


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
    create_tourist()

# def teardown_module(module):
#     TODO - delete both account and tourist

# @pytest.fixture(autouse=True)
# def setup_and_teardown():
#     create_customer()
#     yield
#     delete_customer()

def create_account():
    global ACCOUNT_ID
    request_url = BASE_URL + "AuthAccount/Registration"
    print("Entering setup")
    response = requests.post(request_url, json=json_for_account_creation)
    #print(response.json())
    ACCOUNT_ID = response.json()["data"]["Id"]
    print(f"Account created with Id = {ACCOUNT_ID}")

def create_tourist():
    global TOURIST_ID
    request_url = BASE_URL + f"Tourist"
    response = requests.post(request_url, json = json_for_tourist_creation)
    print("Tourist created")
    #print(response.json())
    TOURIST_ID = response.json()["id"]
    print(f"Tourist created with id = {TOURIST_ID}")

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
    response = requests.post(request_url, json=json_correct_email_and_password)
    print(response.json())
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


# def delete_tourist(id):
#     request_url = BASE_URL + f"Tourist/{id}"
#     response = requests.delete(request_url)
#     print("Customer deleted")
#     print(response.json())


def test_get_correct_tourist_by_id():
    request_url = BASE_URL + f"Tourist/{TOURIST_ID}"
    response = requests.get(request_url)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["id"] == TOURIST_ID
    assert response.json()["tourist_name"] == tourist_name
    assert response.json()["tourist_email"] == tourist_email
    assert response.json()["tourist_location"] == tourist_location
    #assert response.json()["createdat"] == tourist_created_date

def test_get_not_existing_tourist_by_id_1():
    '''If the requested id is existing_id + 4 zeroes then the response is 400 with json'''
    print(f"Existing tourist_id is {TOURIST_ID}")
    request_url = BASE_URL + f"Tourist/{TOURIST_ID}" + "0000"
    print(f"Requested URL is: {request_url}")
    response = requests.get(request_url)
    print(response.text)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["Message"] == "The request is invalid."


def test_get_not_existing_tourist_by_id_2():
    '''If the requested id is existing_id + 1 zero then the response is 404 without json'''
    print(f"Existing tourist_id is {TOURIST_ID}")
    request_url = BASE_URL + f"Tourist/{TOURIST_ID}" + "0"
    print(f"Requested URL is: {request_url}")
    response = requests.get(request_url)

    assert response.status_code == 404

