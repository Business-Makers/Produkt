"""import httpx
import pytest
from httpx import AsyncClient



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login/", json={"username": "user", "password": "pass"})
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/register/", json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        })
        assert response.status_code == 200
        assert response.json() == {"message": "User registered successfully."}
"""