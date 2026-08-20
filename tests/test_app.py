import importlib
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTEMASTER_DB", str(tmp_path / "test.db"))
    import app as app_module
    importlib.reload(app_module)
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as client:
        yield client


def connexion(client, login, password):
    return client.post("/login", data={"login": login, "password": password}, follow_redirects=True)


def test_page_de_connexion(client):
    reponse = client.get("/login")
    assert reponse.status_code == 200
    assert "Connexion" in reponse.get_data(as_text=True)


def test_mauvais_mot_de_passe(client):
    reponse = connexion(client, "lea.santoni", "pas-le-bon")
    assert "incorrect" in reponse.get_data(as_text=True)


def test_eleve_voit_ses_notes(client):
    reponse = connexion(client, "lea.santoni", "lea2026")
    page = reponse.get_data(as_text=True)
    assert "Notes de Léa Santoni" in page
    assert "Partiel tris" in page


def test_prof_voit_ses_evaluations(client):
    reponse = connexion(client, "m.rossi", "algo2026")
    assert "Mes évaluations" in reponse.get_data(as_text=True)


def test_prof_recherche_un_eleve(client):
    connexion(client, "m.rossi", "algo2026")
    reponse = client.get("/prof/recherche?q=Leca")
    assert "Tom Leca" in reponse.get_data(as_text=True)


def test_route_de_sante(client):
    assert client.get("/sante").get_json()["statut"] == "ok"
