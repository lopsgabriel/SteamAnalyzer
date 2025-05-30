import pytest
from unittest.mock import patch, AsyncMock
from rest_framework.response import Response
from Steamlyzer.services import games 
import aiohttp
import json
from pprint import pprint
@pytest.mark.asyncio # Marcador que indica que a função é assicrona
async def test_fetch_game_genres():
  """Testa a funcao fetch_game_genres"""
  game = {'appid': 730}
  mock_response = AsyncMock() # Cria um objeto mock que simula uma resposta da API da Steam
  mock_response.status = 200 # Define o status da resposta da API que é 200
  steam_data = {
    game['appid']: {
      "data": {
        "categories": [{'id': 1, 'description': 'Categoria 1'}, {'id': 2, 'description': 'Categoria 2'}],
        "genres": [{'id': 1, 'description': 'Genero 1'}, {'id': 2, 'description': 'Genero 2'}]
      }
    }
  }
  mock_response.text.return_value = json.dumps(steam_data)
  expected_result = {'categories': ['Categoria 1', 'Categoria 2'], 'genres': ['Genero 1', 'Genero 2']}
  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))):
    async with aiohttp.ClientSession() as session:
      result = await games.fetch_game_genres(session, game)
      assert result == expected_result


@pytest.mark.asyncio
async def test_fetch_game_genres_api_error():
  game = {'appid': 730}
  mock_response = AsyncMock()
  mock_response.status = 500
  mock_response.text.return_value = "Erro simulado"
  expected_result = {'categories': '', 'genres': ''}
  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))):
    async with aiohttp.ClientSession() as session:
      result = await games.fetch_game_genres(session, game)
      assert result == expected_result

@pytest.mark.asyncio
async def test_fetch_details():
  steam_id = "123456789"
  game1 = {
    'appid': 730,
    'name': 'Counter-Strike: Global Offensive',
    'img_icon_url': '730',
    'playtime_forever': 180, 
    
  }
  mock_fetch_game_genres = AsyncMock(return_value={'categories': ['Categoria 1', 'Categoria 2'], 'genres': ['Genero 1', 'Genero 2']})
  mock_response = AsyncMock()
  mock_response.status = 200
  mock_response.json.return_value = {
    "playerstats": {
      "achievements": [
        {"apiname": "apiname1", "achieved": 1, "unlocktime": 1},
        {"apiname": "apiname2", "achieved": 0, "unlocktime": 2},
      ]
    }
  }
  most_played_games = [game1]
  expected_result = {
    "game": "Counter-Strike: Global Offensive",
    "image": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/730/730.jpg",
    "appid": 730,
    "total_achieved": 2,
    "progress_achievements": 50,
    "hours": 3,
    "categories": ['Categoria 1', 'Categoria 2'],
    "genres": ['Genero 1', 'Genero 2']
  }

  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))), \
     patch("Steamlyzer.services.games.fetch_game_genres", new = mock_fetch_game_genres):
    async with aiohttp.ClientSession() as session:
      result = await games.fetch_details(session, game1, steam_id, most_played_games)
      print(result)
      assert result == expected_result

@pytest.mark.asyncio
async def test_fetch_details_low_playtime():
  steam_id = "123456789"
  game1 = {
    'appid': 730,
    'name': 'Counter-Strike: Global Offensive',
    'img_icon_url': '730',
    'playtime_forever': 10, 
    
  }
  mock_fetch_game_genres = AsyncMock(return_value={'categories': ['Categoria 1', 'Categoria 2'], 'genres': ['Genero 1', 'Genero 2']})
  mock_response = AsyncMock()
  mock_response.status = 200
  mock_response.json.return_value = {
    "playerstats": {
      "achievements": []
    }
  }
  most_played_games = [game1]
  expected_result = {
    "game": "Counter-Strike: Global Offensive",
    "image": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/730/730.jpg",
    "appid": 730,
    "total_achieved": 0,
    "progress_achievements": 0,
    "hours": 0,
    "categories": [],
    "genres": []
  }

  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))), \
     patch("Steamlyzer.services.games.fetch_game_genres", new = mock_fetch_game_genres):
    async with aiohttp.ClientSession() as session:
      result = await games.fetch_details(session, game1, steam_id, most_played_games)
      print(result)
      assert result == expected_result

@pytest.mark.asyncio
async def test_fetch_details_achievements_error():
  steam_id = "123456789"
  game1 = {
    'appid': 730,
    'name': 'Counter-Strike: Global Offensive',
    'img_icon_url': '730',
    'playtime_forever': 180, 
    
  }
  mock_fetch_game_genres = AsyncMock(return_value={'categories': ['Categoria 1', 'Categoria 2'], 'genres': ['Genero 1', 'Genero 2']})
  mock_response = AsyncMock()
  mock_response.status = 500
  mock_response.json.return_value = { "error": "Internal Server Error" }
  most_played_games = [game1]
  expected_result = {
    "game": "Counter-Strike: Global Offensive",
    "image": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/730/730.jpg",
    "appid": 730,
    "total_achieved": 0,
    "progress_achievements": 0,
    "hours": 3,
    "categories": ['Categoria 1', 'Categoria 2'],
    "genres": ['Genero 1', 'Genero 2']
  }

  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))), \
     patch("Steamlyzer.services.games.fetch_game_genres", new = mock_fetch_game_genres):
    async with aiohttp.ClientSession() as session:
      result = await games.fetch_details(session, game1, steam_id, most_played_games)
      print(result)
      assert result == expected_result

@pytest.mark.asyncio
async def test_fetch_details_game_not_in_most_played_games():
  steam_id = "123456789"
  game1 = {
    'appid': 730,
    'name': 'Counter-Strike: Global Offensive',
    'img_icon_url': '730',
    'playtime_forever': 180, 
    
  }
  mock_fetch_game_genres = AsyncMock(return_value={'categories': ['Categoria 1', 'Categoria 2'], 'genres': ['Genero 1', 'Genero 2']})
  mock_response = AsyncMock()
  mock_response.status = 200
  mock_response.json.return_value = {
    "playerstats": {
      "achievements": [
        {"apiname": "apiname1", "achieved": 1, "unlocktime": 1},
        {"apiname": "apiname2", "achieved": 0, "unlocktime": 2},
      ]
    }
  }
  most_played_games = []
  expected_result = {
    "game": "Counter-Strike: Global Offensive",
    "image": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/730/730.jpg",
    "appid": 730,
    "total_achieved": 0,
    "progress_achievements": 0,
    "hours": 3,
    "categories": ['Categoria 1', 'Categoria 2'],
    "genres": ['Genero 1', 'Genero 2']
  }

  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))), \
     patch("Steamlyzer.services.games.fetch_game_genres", new = mock_fetch_game_genres):
    async with aiohttp.ClientSession() as session:
      result = await games.fetch_details(session, game1, steam_id, most_played_games)
      print(result)
      assert result == expected_result

@pytest.mark.asyncio
async def test_fetch_details_low_playtime_not_in_most_played_games():
  steam_id = "123456789"
  game1 = {
    'appid': 730,
    'name': 'Counter-Strike: Global Offensive',
    'img_icon_url': '730',
    'playtime_forever': 10, 
    
  }
  mock_fetch_game_genres = AsyncMock(return_value={'categories': ['Categoria 1', 'Categoria 2'], 'genres': ['Genero 1', 'Genero 2']})
  most_played_games = []
  expected_result = {
    "game": "Counter-Strike: Global Offensive",
    "image": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/730/730.jpg",
    "appid": 730,
    "total_achieved": 0,
    "progress_achievements": 0,
    "hours": 0,
    "categories": [],
    "genres": []
  }
  
  with patch("Steamlyzer.services.games.fetch_game_genres", new = mock_fetch_game_genres):
    async with aiohttp.ClientSession() as session:
      result = await games.fetch_details(session, game1, steam_id, most_played_games)
      print(result)
      assert result == expected_result
