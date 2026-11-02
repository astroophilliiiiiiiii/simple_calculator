# -*- coding: utf-8 -*-
import pytest
from fastapi.testclient import TestClient
from inventory_api.main import app

client = TestClient(app)


def test_create_item_valid():
    payload = {'name': 'Widget', 'quantity': 10}
    response = client.post('/items/', json=payload)
    assert response.status_code == 201
    assert response.json() == payload


@pytest.mark.parametrize('name', ['', '   ', '\n\t'])
def test_create_item_invalid_name(name):
    payload = {'name': name, 'quantity': 5}
    response = client.post('/items/', json=payload)
    assert response.status_code == 422


def test_create_item_negative_quantity():
    payload = {'name': 'Gadget', 'quantity': -3}
    response = client.post('/items/', json=payload)
    assert response.status_code == 422
