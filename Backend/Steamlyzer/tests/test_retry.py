import pytest
from Steamlyzer.utils.retry import make_request_with_retry
from unittest.mock import AsyncMock, patch, Mock

def test_make_request():
  """Testa a funcao make_request_with_retry"""
  # Cria uma url de teste
  url = "https://url-teste"
  # Cria um objeto mock que simula uma resposta a url
  mock_response = Mock()
  # Define o status da resposta da API que é 200
  mock_response.status_code = 200
  # Define o conteudo da resposta da API quando a função json() é chamada
  mock_response.json.return_value = {"response": "mocked response"}

  # Substitui o requests.get por um mock
  with patch("requests.get", return_value=mock_response) as mock_get:
    # Chama a funcao
    result = make_request_with_retry(url)
    # Verifica se a funcao retornou o valor esperado
    assert result == {"response": "mocked response"}
    # Verifica se a funcao requests.get foi chamada uma vez
    assert mock_get.call_count == 1

def test_make_request_succeeds_after_retries():
  """Testa a funcao make_request_with_retry e retorna response só depois de duas falhas"""
  url = "https://url-teste"
  # Cria um objeto mock que dá erro com status code 500 para simular uma falha
  mock1_response = Mock()
  mock1_response.status_code = 500
  # Cria um segundo objeto mock que dá erro com status code 500 para simular uma falha
  mock2_response = Mock()
  mock2_response.status_code = 500
  mock_response = Mock()
  mock_response.status_code = 200
  mock_response.json.return_value = {"response": "mocked response"}

  # Substitui o requests.get por um side_effect que retorna os mocks
  with patch("requests.get", side_effect=[mock1_response, mock2_response, mock_response]) as mock_get:
    result = make_request_with_retry(url)
    assert result == {"response": "mocked response"}
    # Verifica se a funcao requests.get foi chamada 3 vezes
    assert mock_get.call_count == 3

def test_make_request_fails():
  """Testa a funcao make_request_with_retry e retorna None se falhar 5 vezes"""
  url = "https://url-teste"
  mock_response = Mock()
  mock_response.status_code = 500
  
  with patch("requests.get", return_value=mock_response) as mock_get:
    result = make_request_with_retry(url)
    assert result is None
    assert mock_get.call_count == 5


