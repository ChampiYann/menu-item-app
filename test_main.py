from fastapi.testclient import TestClient
from fastapi import status
from uuid import uuid4

from main import app

client = TestClient(app)


def test_read_menu_items():
    response = client.get("/menuitems")
    assert response.status_code == status.HTTP_200_OK


def test_create_menu_item():
    test_menuItemIn = {"naam": "bier", "omschrijving": "Dit is een biertje.", "prijs": 2.5, "allergenen": [
        "gluten", "alkohol"], "urlPlaatje": "https://fr.m.wikipedia.org/wiki/Fichier:Pilsner_Bier.jpg"}
    response = client.post("/menuitem", json=test_menuItemIn)
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()
    assert response.json()["naam"] == test_menuItemIn["naam"]
    assert response.json()["omschrijving"] == test_menuItemIn["omschrijving"]
    assert response.json()["prijs"] == test_menuItemIn["prijs"]
    assert response.json()["allergenen"] == test_menuItemIn["allergenen"]
    assert response.json()["urlPlaatje"] == test_menuItemIn["urlPlaatje"]


def test_create_minimum_menu_item():
    test_menuItemIn = {"naam": "bier", "prijs": 2.5}
    response = client.post("/menuitem", json=test_menuItemIn)
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()
    assert response.json()["naam"] == test_menuItemIn["naam"]
    assert response.json()["omschrijving"] == None
    assert response.json()["prijs"] == test_menuItemIn["prijs"]
    assert response.json()["allergenen"] == None
    assert response.json()["urlPlaatje"] == None


def test_create_menu_item_no_naam():
    test_menuItemIn = {"prijs": 2.5}
    response = client.post("/menuitem", json=test_menuItemIn)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_menu_item_no_prijs():
    test_menuItemIn = {"naam": "bier"}
    response = client.post("/menuitem", json=test_menuItemIn)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_menu_item_bad_prijs():
    test_menuItemIn = {"naam": "bier", "omschrijving": "Dit is een biertje.", "prijs": "string", "allergenen": [
        "gluten", "alkohol"], "urlPlaatje": "https://fr.m.wikipedia.org/wiki/Fichier:Pilsner_Bier.jpg"}
    response = client.post("/menuitem", json=test_menuItemIn)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_menu_item_bad_allergenen():
    test_menuItemIn = {"naam": "bier", "omschrijving": "Dit is een biertje.", "prijs": 2.5,
                       "allergenen": "gluten", "urlPlaatje": "https://fr.m.wikipedia.org/wiki/Fichier:Pilsner_Bier.jpg"}
    response = client.post("/menuitem", json=test_menuItemIn)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_menu_item_bad_urlPlaatje():
    test_menuItemIn = {"naam": "bier", "omschrijving": "Dit is een biertje.", "prijs": 2.5, "allergenen": [
        "gluten", "alkohol"], "urlPlaatje": "string"}
    response = client.post("/menuitem", json=test_menuItemIn)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_menu_item():
    test_menuItemIn = {"naam": "bier", "omschrijving": "Dit is een biertje.", "prijs": 2.5, "allergenen": [
        "gluten", "alkohol"], "urlPlaatje": "https://fr.m.wikipedia.org/wiki/Fichier:Pilsner_Bier.jpg"}
    response = client.post("/menuitem", json=test_menuItemIn)
    menuItem_id = response.json()["id"]
    response = client.get("/menuitem/" + menuItem_id)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == menuItem_id
    assert response.json()["naam"] == test_menuItemIn["naam"]
    assert response.json()["omschrijving"] == test_menuItemIn["omschrijving"]
    assert response.json()["prijs"] == test_menuItemIn["prijs"]
    assert response.json()["allergenen"] == test_menuItemIn["allergenen"]
    assert response.json()["urlPlaatje"] == test_menuItemIn["urlPlaatje"]


def test_read_menu_item_bad_id():
    response = client.get("/menuitem/" + "string")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_menu_item_nonexistant_id():
    response = client.get("/menuitem/" + str(uuid4()))
    assert response.status_code == status.HTTP_404_NOT_FOUND
