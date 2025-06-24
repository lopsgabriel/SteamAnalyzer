import pytest
from rest_framework.test import APIClient
from rest_framework.response import Response
from unittest.mock import patch, Mock
import os

os.environ.setdefault("SECRET_KEY", "test")


@pytest.mark.django_db
def test_analyze_valid_steam_id():
  client = APIClient()
  steam_id = "valid_id"
  user_profile = {
    "response": {
      "players": [
        {
          "personaname": "User",
          "timecreated": 1_600_000_000,
          "avatarfull": "url",
          "communityvisibilitystate": 3
        }
      ]
    }
  }
  games_resp = Mock()
  games_resp.status_code = 200
  games_resp.json.return_value = {
    "response": {
      "games": [
        {"appid": 1, "name": "Game 1", "img_icon_url": "1", "playtime_forever": 300}
      ]
    }
  }
  games_data = [
    {
      "game": "Game 1",
      "image": "url",
      "appid": 1,
      "total_achieved": 0,
      "progress_achievements": 0,
      "hours": 5,
      "categories": ["PvP"],
      "genres": ["Action"]
    }
  ]
  ai_output = {
    "steamHistory": "h",
    "topGames": "t",
    "genreStats": "g",
    "categoryStats": "c"
  }
  with patch("Steamlyzer.views.verify_steamid_or_vanity_url", return_value="123"), \
       patch("Steamlyzer.views.gather_user_profile", return_value=user_profile), \
       patch("Steamlyzer.views.requests.get", return_value=games_resp), \
       patch("Steamlyzer.views.gather_data_in_batches", return_value=games_data), \
       patch("Steamlyzer.views.define_player_type", return_value="casual"), \
       patch("Steamlyzer.views.ai_responses", return_value=ai_output):
    response = client.get("/steam/analyze/", {"steam_id": steam_id})
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["steam_id"] == "123"
    assert data["AI_response"] == ai_output


def test_analyze_invalid_steam_id():
  client = APIClient()
  with patch("Steamlyzer.views.verify_steamid_or_vanity_url", return_value=None):
    response = client.get("/steam/analyze/", {"steam_id": "invalid"})
    assert response.status_code == 400
    assert "error" in response.json()


def test_analyze_missing_steam_id():
  client = APIClient()
  response = client.get("/steam/analyze/")
  assert response.status_code == 400
  assert "error" in response.json()


@pytest.mark.django_db
def test_analyze_profile_error():
  client = APIClient()
  with patch("Steamlyzer.views.verify_steamid_or_vanity_url", return_value="123"), \
       patch("Steamlyzer.views.gather_user_profile", return_value=Response({"error": "fail"}, status=500)):
    response = client.get("/steam/analyze/", {"steam_id": "valid"})
    assert response.status_code == 500
    assert "error" in response.json()