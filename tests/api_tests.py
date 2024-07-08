import requests
import pytest

# more mf tests on my mf live deployment. Im tired of this man

BASE_URL = "https://task-2-production-3b3f.up.railway.app"  # pipeops see your mate na.stop giving me 500 unnecesarily please

USER_DATA = {
    "firstName": "mentor",
    "lastName": "shully",
    "email": "mentorshully101@example.com",
    "password": "password123",
    "phone": "1234567890"
}

NEW_ORG_DATA = {
    "name": "Some damn new organisation",
    "description": "This is an organisation but the question you should be asking is are you organised, are you?"
}

ACCESS_TOKEN = None
USER_ID = None
ORG_ID = None

def test_register():
    global ACCESS_TOKEN, USER_ID
    response = requests.post(f"{BASE_URL}/auth/register", json=USER_DATA)
    assert response.status_code == 201
    data = response.json()
    ACCESS_TOKEN = data["data"]["accessToken"]
    USER_ID = data["data"]["user"]["userId"]

def test_login():
    global ACCESS_TOKEN
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": USER_DATA["email"], "password": USER_DATA["password"]})
    assert response.status_code == 200
    data = response.json()
    ACCESS_TOKEN = data["data"]["accessToken"]

def test_get_user():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/users/{USER_ID}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["email"] == USER_DATA["email"]

def test_create_organisation():
    global ORG_ID
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.post(f"{BASE_URL}/api/organisations", json=NEW_ORG_DATA, headers=headers)
    assert response.status_code == 201
    data = response.json()
    ORG_ID = data["data"]["orgId"]

def test_get_organisations():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/organisations", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert any(org["name"] == NEW_ORG_DATA["name"] for org in data["data"]["organisations"])

def test_get_organisation():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{BASE_URL}/api/organisations/{ORG_ID}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == NEW_ORG_DATA["name"]

def test_add_user_to_organisation():
    # this test dey give headeache walai. adding more debug print statements
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {"userId": USER_ID}
    print(f"Adding user to organisation: {data}")
    response = requests.post(f"{BASE_URL}/api/organisations/{ORG_ID}/users", json=data, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json()}")
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main(["-v", __file__])
