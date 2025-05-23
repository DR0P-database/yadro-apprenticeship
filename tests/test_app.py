from random_user_app.routes.base import app
from fastapi.testclient import TestClient      

client = TestClient(app)


def test_root_redirect():
    respone = client.get('/')
    assert respone.status_code == 307

def test_get_homepage():
    respones = client.get('/homepage')
    assert respones.status_code == 200
    assert "<html" in respones.text