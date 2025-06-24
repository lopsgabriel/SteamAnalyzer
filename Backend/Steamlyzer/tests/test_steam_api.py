"""Testes para o módulo ``steam_api``."""
import pytest
from unittest.mock import patch, AsyncMock
from rest_framework.response import Response
from Steamlyzer.services import steam_api

@pytest.mark.asyncio
def test_resolve_vanity_url():
  """Verifica se URLs personalizadas são convertidas corretamente em SteamID."""
  custom_url = "custom_url"
  expected_steam_id = "123456789"
  
  mock_response = {
    "response": {
      "success": 1,
      "steamid": expected_steam_id
    }
  }
  with patch("Steamlyzer.services.steam_api.make_request_with_retry", return_value=mock_response):
    result = steam_api.resolve_vanity_url(custom_url)
    assert result == expected_steam_id

@pytest.mark.asyncio
def test_resolve_vanity_invalid_url():
  """Garante que URLs inválidas retornam ``None``."""
  custom_url = "custom_invalid_url"
  mock_response = {
    "response": {
      "success": 2,
      "steamid": "no match"
    }
  }

  with patch("Steamlyzer.services.steam_api.make_request_with_retry", return_value=mock_response):
    result = steam_api.resolve_vanity_url(custom_url)
    assert result == None

@pytest.mark.asyncio
def test_resolve_vanity_none_response():
  """Retorna ``None`` quando a API responde com erro."""
  custom_url = "custom_invalid_url"
  mock_response = {"error": "Error"}

  with patch("Steamlyzer.services.steam_api.make_request_with_retry", return_value=mock_response):
    result = steam_api.resolve_vanity_url(custom_url)
    assert result == None

@pytest.mark.asyncio
def test_verify_raw_steamid64_input():
  """Deve retornar o SteamID quando o valor passado já é um ID válido."""
  raw = "123456789"
  mock_response = raw

  with patch("Steamlyzer.services.steam_api.resolve_vanity_url", return_value=mock_response):
    result = steam_api.verify_steamid_or_vanity_url(raw)
    assert result == raw

@pytest.mark.asyncio
def	test_verify_steamid_from_profile_url():
  """Extrai o SteamID quando a URL contém /profiles/."""
  raw = "steamcommunity.com/profiles/76561198000000000"
  mock_response = '76561198000000000'

  with patch("Steamlyzer.services.steam_api.resolve_vanity_url", return_value=mock_response):
    result = steam_api.verify_steamid_or_vanity_url(raw)
    assert result == mock_response

@pytest.mark.asyncio
def	test_verify_vanity_from_custom_url():
  """Converte URLs do tipo /id/ em SteamID."""
  raw = "steamcommunity.com/id/custom"
  mock_response = '76561198000000000'

  with patch("Steamlyzer.services.steam_api.resolve_vanity_url", return_value=mock_response):
    result = steam_api.verify_steamid_or_vanity_url(raw)
    assert result == mock_response

@pytest.mark.asyncio
def	test_verify_raw_vanity_input():
  raw = "custom123"
  """Retorna ``None`` para entradas de vanity inválidas."""
  mock_response = None

  with patch("Steamlyzer.services.steam_api.resolve_vanity_url", return_value=mock_response):
    result = steam_api.verify_steamid_or_vanity_url(raw)
    assert result == mock_response

@pytest.mark.asyncio
def	test_verify_invalid_input_returns_none():
  """Entradas não textuais devem resultar em ``None``."""
  raw = {"invalid": "input"}
  mock_response = None

  with patch("Steamlyzer.services.steam_api.resolve_vanity_url", return_value=mock_response):
    result = steam_api.verify_steamid_or_vanity_url(raw)
    assert result == mock_response