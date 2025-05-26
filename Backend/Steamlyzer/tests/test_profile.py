import pytest
from unittest.mock import patch, AsyncMock
from rest_framework.response import Response
from Steamlyzer.services import profile
import aiohttp
import asyncio

@pytest.mark.asyncio # Marcador que indica que a função é assicrona
async def test_fetch_user_profile():
  """Testa a funcao fetch_user_profile"""
  steam_id = "123456789"
  mock_response = AsyncMock() # Cria um objeto mock que simula uma resposta da API da Steam
  mock_response.status = 200 # Define o status da resposta da API que é 200
  mock_response.json.return_value = {
    # Define o conteudo da resposta da API quando a função json() é chamada
      "response": {
          "players": [
              {
                  "communityvisibilitystate": 3
              }
          ]
      }
  }

  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))): #Substitui o ClientSession.get por um AsyncMock. O aiohttp.ClientSession.get aponta para o metodo get. O return_value=AsyncMock(...) é o valor retornado sempre que o session.get ser chamado. O __aenter__=AsyncMock(return_value=mock_response) faz com que o resp da função seja mock_response
    async with aiohttp.ClientSession() as session:
      result = await profile.fetch_user_profile(session, steam_id) # Na hora que a função  chamar session.get(url), o mock_response será retornado
      assert "response" in result
      assert "players" in result["response"]


@pytest.mark.asyncio # Marcador que indica que a função é assicrona
async def test_fetch_user_profile_private():
  """Testa a funcao fetch_user_profile"""
  steam_id = "123456789"
  mock_response = AsyncMock() # Cria um objeto mock que simula uma resposta da API da Steam
  mock_response.status = 200 # Define o status da resposta da API que é 200
  mock_response.json.return_value = {
    # Define o conteudo da resposta da API quando a função json() é chamada
      "response": {
          "players": [
              {
                  "communityvisibilitystate": 1
              }
          ]
      }
  }

  with patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))): #Substitui o ClientSession.get por um AsyncMock. O aiohttp.ClientSession.get aponta para o metodo get. O return_value=AsyncMock(...) é o valor retornado sempre que o session.get ser chamado. O __aenter__=AsyncMock(return_value=mock_response) faz com que o resp da função seja mock_response
    async with aiohttp.ClientSession() as session:
      result = await profile.fetch_user_profile(session, steam_id) # Na hora que a função  chamar session.get(url), o mock_response será retornado
      assert isinstance(result, Response) # Verifica se result é uma instancia(objeto criado) da classe Response
      assert result.status_code == 403 # Verifica se o status code da resposta é 403, result contem apenas status_code e data(que é um dicionario com mensagem de erro)
      assert "error" in result.data

@pytest.mark.asyncio
async def test_fetch_user_profile_api_error():
  steam_id = "123456789"
  mock_response = AsyncMock()
  mock_response.status = 500
  mock_response.text.return_value = "Erro simulado"

  with patch("Steamlyzer.services.profile.make_request_with_retry", return_value=None), \
    patch("aiohttp.ClientSession.get", return_value=AsyncMock(__aenter__=AsyncMock(return_value=mock_response))):
    async with aiohttp.ClientSession() as session:
      result = await profile.fetch_user_profile(session, steam_id)
      assert isinstance(result, Response)
      assert result.status_code == 500
      assert "error" in result.data

@pytest.mark.asyncio
async def test_gather_user_profile():
  steam_id = "123456789"
  expected_data = {"mocked": "data"}

  with patch("Steamlyzer.services.profile.fetch_user_profile", new = AsyncMock(return_value=expected_data)):
    result = await profile.gather_user_profile(steam_id)
    assert result == expected_data