from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)


def test_marseille_win():
    response = client.get("/probability/?bet_id=1&outcome_id=1")
    assert response.status_code == 200
    assert "probability" in response.json()
    # Vous pouvez ajouter d'autres assertions en fonction de vos attentes.

def test_draw():
    response = client.get("/probability/?bet_id=1&outcome_id=2")
    assert response.status_code == 200
    assert "probability" in response.json()
    # Comme la probabilité calculée est de 0.28, vous pouvez ajouter :
    assert response.json()["probability"] == 0.28

# Continuez avec d'autres scénarios...
