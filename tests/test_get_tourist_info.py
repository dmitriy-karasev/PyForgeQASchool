import requests
# import pytest
from faker import Faker
from datetime import datetime

# automated tests for tourist GET endpoint /api/Toutist/{id}
# getting info about existing tourist
# in setup we create new tourist and then query its info through GET request

BASE_URL = "http://restapi.adequateshop.com/api/"
TOURIST_ID = None

fake = Faker()

tourist_name = fake.name()
tourist_email = fake.email()
tourist_created_date = datetime.utcnow().isoformat().replace("+00:00", "Z")
tourist_location = "Earth"

print(f"Generated data for tourist creation are: name {tourist_name}, email {tourist_email}, \
      tourist_location {tourist_location}, created time {tourist_created_date}")

json_for_tourist_creation = {
  "id": 0,
  "tourist_name": tourist_name,
  "tourist_email": tourist_email,
  "tourist_location": tourist_location,
  "createdat": tourist_created_date
}

def setup_module(module):
    create_tourist()

# currently this service, i.e. DELETE is not provided
# def teardown_module(module):
#     delete_tourist()



def create_tourist():
    '''Tourist creation'''
    global TOURIST_ID
    request_url = BASE_URL + f"Tourist"
    response = requests.post(request_url, json = json_for_tourist_creation)
    TOURIST_ID = response.json()["id"]
    print(f"New tourist created with id = {TOURIST_ID} in setup")


# def delete_tourist(id):
#     request_url = BASE_URL + f"Tourist/{id}"
#     response = requests.delete(request_url)
#     print("Tourist deleted")
#     print(response.json())


def test_get_correct_tourist_by_id():
    '''Tests correct data is returned for existing tourist'''
    request_url = BASE_URL + f"Tourist/{TOURIST_ID}"
    response = requests.get(request_url)
    print(f"Received response is {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == TOURIST_ID
    assert response.json()["tourist_name"] == tourist_name
    assert response.json()["tourist_email"] == tourist_email
    assert response.json()["tourist_location"] == tourist_location
    #assert response.json()["createdat"] == tourist_created_date

def test_get_not_existing_tourist_400_by_id():
    '''Tests correct response, 400 for non-existing tourist_id'''
    '''If the requested id is existing_id + 4 zeroes then the response is 400 with json'''
    '''Seems that internally there are 2 separate cases on how to treat
    requests for non-existing tourits_id. So 2 test casea are provided
    Ideally the response should be the same.'''
    print(f"Existing tourist_id is {TOURIST_ID}")
    request_url = BASE_URL + f"Tourist/{TOURIST_ID}" + "0000"
    print(f"Requested URL is: {request_url}")
    response = requests.get(request_url)
    print(f"Received response is {response.json()}")
    assert response.status_code == 400
    assert response.json()["Message"] == "The request is invalid."


def test_get_not_existing_tourist_404_by_id():
    '''Tests correct response, 400 for non-existing tourist_id'''
    '''If the requested id is existing_id + 1 zero then the response is 404 without json'''
    print(f"Existing tourist_id is {TOURIST_ID}")
    request_url = BASE_URL + f"Tourist/{TOURIST_ID}" + "0"
    print(f"Requested URL is: {request_url}")
    response = requests.get(request_url)
    print(f"Returned status code is {response.status_code}")
    assert response.status_code == 400
    assert response.json()["Message"] == "The request is invalid."

