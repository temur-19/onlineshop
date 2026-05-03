import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from db.db import Base, get_db
from main import app

load_dotenv()

DATABASE_URL = os.getenv("TEST_DATABASE_URL")


test_engine = create_async_engine(DATABASE_URL,
                       connect_args={'check_same_thread': False},
                       echo=True)

TestSession = async_sessionmaker(bind=test_engine, autoflush=False)

async def override_get_db():
    async with TestSession() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())


test_client = TestClient(app)


def test_create_user():
    response = test_client.post("/api/register/", json={"username": "testuser3",
                                                     "password": "testpassword",
                                                     "email": "Test"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser3"


def test_login():
    response = test_client.post("/api/login/", data={"username": "Test", "password": "testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user():
    # 1. Login holatini tekshiring
    login_response = test_client.post("/api/login/", data={"username": "Test", "password": "testpassword"})
    print(f"Login status: {login_response.status_code}")
    print(f"Login body: {login_response.json()}")
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 2. User_me so'rovini yuborish (Metodni GET/POST ekanini aniqlang)
    response = test_client.get("/api/user_me/", headers={"Authorization": f"Bearer {token}"})
    
    if response.status_code == 401:
        print(f"Xato sababi: {response.json()}") # API nima uchun rad etganini ko'rsatadi
        
    assert response.status_code == 200

def test_create_product():
    login_response = test_client.post("/api/login/", data={"username": "Test", "password": "testpassword"})
    token = login_response.json()["access_token"]           

def test_create_order():
    login_response = test_client.post("/api/login/", data={"username": "Test", "password": "testpassword"})
    token = login_response.json()["access_token"]           