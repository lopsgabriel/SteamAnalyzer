import pytest
from unittest.mock import patch, AsyncMock
from rest_framework.response import Response
from Steamlyzer.services import ai_responses

def test_formatted_category():
  categorias = { 'categoria 1' : 100 }
  expected_output = 'Top 5 categorias mais jogadas: categoria 1: 100.00h'
  assert ai_responses.formatted_category(categorias) == expected_output

def test_formatted_genre():
  genres = { 'genre 1' : 100, 'genre 2': 200 }
  expected_output = 'Top 5 gêneros mais jogados: genre 2: 200.00h, genre 1: 100.00h'
  assert ai_responses.formatted_genre(genres) == expected_output

def test_formatted_top5Games():
  games = [ { 'game': 'game 1', 'hours': 350 }, { 'game': 'game 2', 'hours': 100 }, { 'game': 'game 3', 'hours': 200 } ]
  expected_output = 'Top 5 jogos mais jogados: game 1: 350.00h, game 3: 200.00h, game 2: 100.00h'
  assert ai_responses.formatted_top5Games(games) == expected_output

class MockResponse:
  def __init__(self, json_data):
    self.json = lambda: json_data

  def json(self):
    return self.json_data
  
def test_category_response():
  username = 'username'
  time_played_per_category = { 'category 1' : 100, 'category 2': 200 }

  mock_ai_response = {
    'candidates': [
      {
        'content': {
          'parts': [
            {
              'text': 'Top 5 categorias mais jogadas: category 1: 100.00h, category 2: 200.00h'
            }
          ]
        }
      }
    ]
  }
 
  with patch("Steamlyzer.services.ai_responses.httpx.post", return_value=MockResponse(mock_ai_response)):
    result = ai_responses.category_response(username, time_played_per_category)
    assert result == mock_ai_response['candidates'][0]['content']['parts'][0]['text']

def test_genre_response():
  username = 'username'
  time_played_per_genre = { 'genre 1' : 100, 'genre 2': 200 }
  total_games = 10
  top_5 = [ { 'game': 'game 1', 'hours': 350 }, { 'game': 'game 2', 'hours': 100 }, { 'game': 'game 3', 'hours': 200 } ]

  mock_ai_response = {
    'candidates': [
      {
        'content': {
          'parts': [
            {
              'text': 'Top 5 gêneros mais jogados: genre 2: 200.00h, genre 1: 100.00h'
            }
          ]
        }
      }
    ]
  }
 
  with patch("Steamlyzer.services.ai_responses.httpx.post", return_value=MockResponse(mock_ai_response)):
    result = ai_responses.genre_response(username, time_played_per_genre, total_games, top_5)
    assert result == mock_ai_response['candidates'][0]['content']['parts'][0]['text']

def test_steamHistory():
  username = 'username'
  date_joined = '2023-01-01'
  total_games = 10
  time_played = 100
  days_on_steam = 10

  mock_ai_response = {
    'candidates': [
      {
        'content': {
          'parts': [
            {
              'text': 'Top 5 jogos mais jogados: game 1: 350.00h, game 3: 200.00h, game 2: 100.00h'
            }
          ]
        }
      }
    ]
  }
 
  with patch("Steamlyzer.services.ai_responses.httpx.post", return_value=MockResponse(mock_ai_response)):
    result = ai_responses.steamHistory_response(username, date_joined, total_games, time_played, days_on_steam)
    assert result == mock_ai_response['candidates'][0]['content']['parts'][0]['text']

def test_top5_response():
  username = 'username'
  top_5 = [ { 'game': 'game 1', 'hours': 350 }, { 'game': 'game 2', 'hours': 100 }, { 'game': 'game 3', 'hours': 200 } ]

  mock_ai_response = {
    'candidates': [
      {
        'content': {
          'parts': [
            {
              'text': 'Top 5 jogos mais jogados: game 1: 350.00h, game 3: 200.00h, game 2: 100.00h'
            }
          ]
        }
      }
    ]
  }
 
  with patch("Steamlyzer.services.ai_responses.httpx.post", return_value=MockResponse(mock_ai_response)):
    result = ai_responses.top5_response(username, top_5)
    assert result == mock_ai_response['candidates'][0]['content']['parts'][0]['text']

def test_ai_responses():
  username = 'username'
  date_joined = '2023-01-01'
  total_games = 10
  time_played = 100
  time_played_per_genre = { 'genre 1' : 100, 'genre 2': 200 }
  time_played_per_category = { 'category 1' : 100, 'category 2': 200 }
  top_5 = [ { 'game': 'game 1', 'hours': 350 }, { 'game': 'game 2', 'hours': 100 }, { 'game': 'game 3', 'hours': 200 } ]
  days_on_steam = 10

  mock_steamHistory_response = 'steamHistory response'
  mock_topGames_response = 'topGames response'
  mock_genreStats_response = 'genreStats response'
  mock_categoryStats_response = 'categoryStats response'
  expected_result = { 'steamHistory': mock_steamHistory_response, 'topGames': mock_topGames_response, 'genreStats': mock_genreStats_response, 'categoryStats': mock_categoryStats_response }

  with patch('Steamlyzer.services.ai_responses.steamHistory_response', return_value=mock_steamHistory_response), \
    patch('Steamlyzer.services.ai_responses.top5_response', return_value=mock_topGames_response), \
    patch('Steamlyzer.services.ai_responses.genre_response', return_value=mock_genreStats_response), \
    patch('Steamlyzer.services.ai_responses.category_response', return_value=mock_categoryStats_response):
    result = ai_responses.ai_responses(username, date_joined, total_games, time_played, time_played_per_genre, time_played_per_category, top_5, days_on_steam)
    assert result == expected_result