import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.core.db import db_manager
import os


@pytest.fixture(scope="module")
def client():
    # Use test database
    os.environ["DB_NAME"] = "poker_test"
    
    app = create_app()
    
    # Initialize test database
    db_manager.init_db()
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Cleanup test data
    # with db_manager.get_cursor() as cursor:
    #     cursor.execute("DELETE FROM hands")


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_hand(client):
    """Test creating a poker hand"""
    hand_data = {
        "stacks": [1000, 1000, 1000, 1000, 1000, 1000],
        "dealer_index": 0,
        "small_blind_index": 1,
        "big_blind_index": 2,
        "actions": ["c", "c", "f", "f", "f", "f"],
        "hole_cards": ["AsKd", "2h3c", "", "", "", ""],
        "board": "Ah2s3d4c5h"
    }
    
    response = client.post("/api/v1/hands/", json=hand_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "id" in result
    assert result["stacks"] == hand_data["stacks"]
    assert result["actions"] == hand_data["actions"]
    assert "winnings" in result
    assert len(result["winnings"]) == 6


def test_get_hands(client):
    """Test getting all hands"""
    # First create a hand
    hand_data = {
        "stacks": [1000, 1000, 1000, 1000, 1000, 1000],
        "dealer_index": 0,
        "small_blind_index": 1,
        "big_blind_index": 2,
        "actions": ["f", "f", "f", "f", "f", "f"],
        "hole_cards": ["", "", "", "", "", ""],
        "board": ""
    }
    
    create_response = client.post("/api/v1/hands/", json=hand_data)
    assert create_response.status_code == 200
    
    # Then get all hands
    response = client.get("/api/v1/hands/")
    assert response.status_code == 200
    
    hands = response.json()
    assert isinstance(hands, list)
    assert len(hands) >= 1


def test_get_hand_by_id(client):
    """Test getting a specific hand by ID"""
    # First create a hand
    hand_data = {
        "stacks": [1000, 1000, 1000, 1000, 1000, 1000],
        "dealer_index": 0,
        "small_blind_index": 1,
        "big_blind_index": 2,
        "actions": ["f", "f", "f", "f", "f", "f"],
        "hole_cards": ["", "", "", "", "", ""],
        "board": ""
    }
    
    create_response = client.post("/api/v1/hands/", json=hand_data)
    assert create_response.status_code == 200
    
    hand_id = create_response.json()["id"]
    
    # Then get the specific hand
    response = client.get(f"/api/v1/hands/{hand_id}")
    assert response.status_code == 200
    
    hand = response.json()
    assert hand["id"] == hand_id
    assert hand["stacks"] == hand_data["stacks"]


def test_get_nonexistent_hand(client):
    """Test getting a hand that doesn't exist"""
    response = client.get("/api/v1/hands/nonexistent-id")
    assert response.status_code == 404


def test_poker_engine_calculations(client):
    """Test that poker engine calculations work"""
    hand_data = {
        "stacks": [1000, 1000, 1000, 1000, 1000, 1000],
        "dealer_index": 0,
        "small_blind_index": 1,
        "big_blind_index": 2,
        "actions": ["c", "c", "x", "x", "x", "x"],
        "hole_cards": ["AsAd", "KsKd", "", "", "", ""],
        "board": "2c3h4d5c6s"
    }
    
    response = client.post("/api/v1/hands/", json=hand_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "winnings" in result
    assert len(result["winnings"]) == 6
    
    # Check that winnings sum to zero (conservation of chips)
    total_winnings = sum(result["winnings"])
    assert abs(total_winnings) <= 1  # Allow for small rounding errors

def test_simulate_full_gameplay(client):
    """Simulate a realistic poker hand with multiple actions and evaluate the result"""
    hand_data = {
        "stacks": [1500, 1500, 1500, 1500, 1500, 1500],
        "dealer_index": 3,
        "small_blind_index": 4,
        "big_blind_index": 5,
        "actions": ["c", "r", "c", "f", "c", "x", "x", "x"],  # Custom realistic action flow
        "hole_cards": ["AhKd", "QcQs", "9c9h", "JdTh", "", ""],
        "board": "2sQd3h8cJc"
    }

    response = client.post("/api/v1/hands/", json=hand_data)
    assert response.status_code == 200, response.text

    result = response.json()
    
    assert "id" in result
    assert isinstance(result["winnings"], list)
    assert len(result["winnings"]) == 6

    # Ensure pot conservation (sum of winnings ≈ 0)
    total_winnings = sum(result["winnings"])
    assert abs(total_winnings) <= 1  # Accept small rounding errors


def test_simulate_multiple_hands(client):
    hands = [
        {
            "stacks": [1000] * 6,
            "dealer_index": 0,
            "small_blind_index": 1,
            "big_blind_index": 2,
            "actions": ["c", "c", "f", "f", "f", "f"],
            "hole_cards": ["AsKd", "2h3c", "", "", "", ""],
            "board": "Ah2s3d4c5h"
        },
        {
            "stacks": [900, 1100, 1000, 1000, 1000, 1000],
            "dealer_index": 1,
            "small_blind_index": 2,
            "big_blind_index": 3,
            "actions": ["c", "r", "f", "f", "c", "x"],
            "hole_cards": ["KhQh", "JcJd", "9s9d", "", "", ""],
            "board": "7h8h9hThJh"
        }
    ]

    for hand_data in hands:
        response = client.post("/api/v1/hands/", json=hand_data)
        assert response.status_code == 200, response.text
        result = response.json()
        assert "winnings" in result
        assert len(result["winnings"]) == 6
        assert abs(sum(result["winnings"])) <= 1
