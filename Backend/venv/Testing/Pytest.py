from httpx import AsyncClient
import pytest
from Backend.venv.Server.main import app  # Stelle sicher, dass deine App korrekt importiert wird


@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register/", json={
            "firstname": "Max",
            "lastname": "Mustermann",
            "birthday": "1990-01-01",
            "email": "max@example.com",
            "phone_number": "0123456789",
            "address": "Musterstraße 1",
            "country": "Deutschland",
            "login_name": "max2024",
            "password": "sehr_sicheres_passwort"
        })
        assert response.status_code == 201
        assert response.json()['message'] == "Registration successful"


@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login/", json={
            "login_name": "max2024",
            "password": "sehr_sicheres_passwort"
        })
        assert response.status_code == 200
        assert 'access_token' in response.json()
