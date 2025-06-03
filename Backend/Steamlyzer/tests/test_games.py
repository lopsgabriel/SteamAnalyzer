import pytest
from unittest.mock import patch, AsyncMock
from rest_framework.response import Response
from Steamlyzer.services import games 
import aiohttp
import json

#-----------------------------------TESTES DE FETCH_GAME_GENRES---------------------------------------------------------

@pytest.mark.asyncio # Marcador que indica que a função é assicrona
async def test_fetch_game_genres():
  """Testa a funcao fetch_game_genres"""
  game = {'appid': 730}
  mock_response = AsyncMock() # Cria um objeto mock que simula uma resposta da API da Steam
  mock_response.status = 200 # Define o status da resposta da API que é 200
  # Estrutura que simula a resposta JSON da Steam
  steam_data = {
      game['appid']: {
          "data": {
              "categories": [{'id': 1, 'description': 'Categoria 1'}, {'id': 2, 'description': 'Categoria 2'}],
              "genres": [{'id': 1, 'description': 'Genero 1'}, {'id': 2, 'description': 'Genero 2'}]
          }
      }
  }

  # Define o retorno do método .text() para a resposta simulada
  mock_response.text.return_value = json.dumps(steam_data)

  # Define o que se espera como retorno da função
  expected_result = {
      'categories': ['Categoria 1', 'Categoria 2'],
      'genres': ['Genero 1', 'Genero 2']
  }

  # Patch na chamada ao aiohttp para que devolva a resposta mockada
  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))):
      async with aiohttp.ClientSession() as session:
          result = await games.fetch_game_genres(session, game)
          assert result == expected_result


@pytest.mark.asyncio
async def test_fetch_game_genres_api_error():
    # Testa a função fetch_game_genres simulando um erro de status na API
    game = {'appid': 730}
    mock_response = AsyncMock()
    mock_response.status = 500  # Status de erro
    mock_response.text.return_value = "Erro simulado"

    # Espera-se que a função retorne valores vazios
    expected_result = {'categories': '', 'genres': ''}

    with patch("Steamlyzer.services.games.make_request_with_retry", return_value=None), \
         patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))):
        async with aiohttp.ClientSession() as session:
            result = await games.fetch_game_genres(session, game)
            assert result == expected_result

#-----------------------------------TESTES DE FETCH_DETAILS-------------------------------------------------------------

@pytest.mark.asyncio
async def test_fetch_details():
    """Testa a funcao fetch_details em condições normais"""
    steam_id = "123456789"
    game1 = {
        'appid': 730,
        'name': 'Counter-Strike: Global Offensive',
        'img_icon_url': '730',
        'playtime_forever': 180,
    }

    # Mock do retorno da função fetch_game_genres
    mock_fetch_game_genres = AsyncMock(return_value={
        'categories': ['Categoria 1', 'Categoria 2'],
        'genres': ['Genero 1', 'Genero 2']
    })

    # Mock da resposta da API de conquistas
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

    most_played_games = [game1]  # Apenas um jogo para facilitar o teste

    # Resultado esperado calculado com base nos dados mockados
    expected_result = {
        "game": "Counter-Strike: Global Offensive",
        "image": "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/730/730.jpg",
        "appid": 730,
        "total_achieved": 2,  # 1 conquistado + 1 não conquistado
        "progress_achievements": 50,  # 1 de 2 = 50%
        "hours": 3,  # 180 minutos = 3h
        "categories": ['Categoria 1', 'Categoria 2'],
        "genres": ['Genero 1', 'Genero 2']
    }

    # Patch no session.get e na função fetch_game_genres
    with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))), \
         patch("Steamlyzer.services.games.fetch_game_genres", new=mock_fetch_game_genres):

        async with aiohttp.ClientSession() as session:
            result = await games.fetch_details(session, game1, steam_id, most_played_games)
            print(result)
            assert result == expected_result


@pytest.mark.asyncio
async def test_fetch_details_low_playtime():
  """Testa a funcao fetch_details com playtime_forever muito baixo"""
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
  """Testa a funcao fetch_details com erro na API da steam ao buscar conquistas"""
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
  """Testa a funcao fetch_details quando o jogo nao esta na lista de jogos mais jogados"""
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
  """Testa a funcao fetch_details quando o jogo nao esta na lista de jogos mais jogados e o playtime é baixo"""
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

#-----------------------------------TESTES DE GATHER_DATA------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gather_data_in_10_batches():
    """Testa a funcao gather_data quando a lista de jogos é muito grande"""
    # Entrada controlada
    games_list = [
      {"appid": 1, "name": "game1", "img_icon_url": "1", "playtime_forever": 500},
      {"appid": 2, "name": "game2", "img_icon_url": "2", "playtime_forever": 300},
      {"appid": 3, "name": "game3", "img_icon_url": "3", "playtime_forever": 100}
    ]
    steam_id = "123456789"
    most_played_games = games_list  # pode ser igual para esse teste

    # Resultado esperado de cada chamada a fetch_details
    mock_game_result = {
        "game": "mocked_game",
        "image": "url",
        "appid": 0,
        "total_achieved": 0,
        "progress_achievements": 0,
        "hours": 0,
        "categories": [],
        "genres": []
    }
    mock_sleep = AsyncMock()

    with patch("Steamlyzer.services.games.sum", return_value=310), \
         patch("Steamlyzer.services.games.fetch_details", new=AsyncMock(return_value=mock_game_result)), \
         patch("asyncio.sleep", new=mock_sleep):
        results = await games.gather_data_in_batches(games_list, steam_id, most_played_games)
        # Verifica se o resultado tem o mesmo tamanho da lista de entrada
        assert len(results) == len(games_list)
        # Verifica quantos batches foram chamados
        assert mock_sleep.call_count == 1
        # Verifica se cada resultado tem o valor mockado
        for res in results:
            assert res["game"] == "mocked_game"

@pytest.mark.asyncio
async def test_gather_data_in_batches():
    """Testa a funcao gather_data_in_batches"""
    games_list = [
      {"appid": 1, "name": "game1", "img_icon_url": "1", "playtime_forever": 500},
      {"appid": 2, "name": "game2", "img_icon_url": "2", "playtime_forever": 300},
      {"appid": 3, "name": "game3", "img_icon_url": "3", "playtime_forever": 100}
    ]
    steam_id = "123456789"
    most_played_games = games_list  

    mock_game_result = {
        "game": "mocked_game",
        "image": "url",
        "appid": 0,
        "total_achieved": 0,
        "progress_achievements": 0,
        "hours": 0,
        "categories": [],
        "genres": []
    }
    mock_sleep = AsyncMock()

    with patch("Steamlyzer.services.games.fetch_details", new=AsyncMock(return_value=mock_game_result)), \
         patch("asyncio.sleep", new=mock_sleep):
        results = await games.gather_data_in_batches(games_list, steam_id, most_played_games)
        assert len(results) == len(games_list)
        assert mock_sleep.call_count == 1
        for res in results:
            assert res["game"] == "mocked_game"

