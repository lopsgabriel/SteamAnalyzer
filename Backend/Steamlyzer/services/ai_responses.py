import httpx
import os
import copy

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}'
headers = {
  'Content-Type': 'application/json'
}
payload_template = {
  "contents": [{
    "parts": [{
        "text": ""
    }]
  }]
}

def formatted_category(categorias: dict, top_n=5) -> str:
    top_categorias = sorted(categorias.items(), key=lambda x: x[1], reverse=True)[:top_n]
    partes = [f"{nome}: {horas:.2f}h" for nome, horas in top_categorias]
    return f"Top {top_n} categorias mais jogadas: " + ", ".join(partes)

def formatted_genre(genres: dict, top_n=5) -> str:
    # Agora você está iterando corretamente sobre (chave, valor)
    top_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)[:top_n]
    partes = [f"{nome}: {horas:.2f}h" for nome, horas in top_genres]
    return f"Top {top_n} gêneros mais jogados: " + ", ".join(partes)

def formatted_top5Games(games: dict, top_n=5) -> str:
    top_games = sorted(games, key=lambda x: x["hours"], reverse=True)[:top_n]
    partes = [f"{game['game']}: {game['hours']:.2f}h" for game in top_games]
    return f"Top {top_n} jogos mais jogados: " + ", ".join(partes)

def category_response(username, time_played_per_category):

  prompt = f'Analise os hábitos de jogo de um usuário com base nesses dados da Steam e faça um comentario. Uma abordagem mais empática, como se fosse algum amigo te analisando de forma leve. Mas também pode fazer piadas. Exemplo: "FIFA e Rocket League no topo? Clássico. Te imagino jogando de fone, xingando juiz invisível, e dizendo só mais uma às 3h da manhã." "Com esse tanto de horas de jogo ja dava pra ter se formado em medicina". Maximo de 300 caracteres, não utilize # e nem emojis, não rir com hahaha, foque na categoria mais jogada, conte uma curiosidade comportamental dos players que jogam a categoria mais jogada dele. -Nome: {username} -{formatted_category(time_played_per_category)} '
  payload = copy.deepcopy(payload_template)
  payload["contents"][0]["parts"][0]["text"] = prompt
  data = httpx.post(url, headers=headers, json=payload).json()
  return data['candidates'][0]['content']['parts'][0]['text']

def genre_response(username, time_played_per_genre, total_games, top_5):
  prompt = f'Analise os hábitos de jogo de um usuário com base nesses dados da Steam e faça um comentario. Uma abordagem mais empática, como se fosse algum amigo te analisando de forma leve e com piadas, foque mais no genero mais jogado não cite os jogos Exemplo: "FIFA e Rocket League no topo? Clássico. Te imagino jogando de fone, xingando juiz invisível, e dizendo só mais uma às 3h da manhã.""Com esse tanto de horas de jogo ja dava pra ter se formado em medicina". Maximo de 300 caracteres, não utilize # e nem emojis. Conte uma curiosidade do tipo de pessao que joga o genero que o usuario mais joga: -Nome: {username} -Total de jogos: {total_games} -{formatted_genre(time_played_per_genre)}  -{formatted_top5Games(top_5)}'
  payload = copy.deepcopy(payload_template)
  payload["contents"][0]["parts"][0]["text"] = prompt
  data = httpx.post(url, headers=headers, json=payload).json()
  return data['candidates'][0]['content']['parts'][0]['text']

def steamHistory_response(username, date_joined, total_games, time_played, days_on_steam):
  prompt = f'Analise os hábitos de jogo de um usuário com base nesses dados da Steam e faça um comentario. Uma abordagem mais empática, como se fosse algum amigo te analisando de forma leve. Mas também pode fazer piadas. Exemplo: "FIFA e Rocket League no topo? Clássico. Te imagino jogando de fone, xingando juiz invisível, e dizendo só mais uma às 3h da manhã." "Com esse tanto de horas de jogo ja dava pra ter se formado em medicina". Maximo de 300 caracteres, não utilize # e nem emojis, não rir com hahaha. Diga a data onde a steam do usuario foi criada, e depois conte uma curiosidade do dia que a steam do usuario foi criada, e faça uma piada com a quantidade de horas jogadas: -Nome: {username} -Total de horas jogadas: {time_played}h -Conta criada em: {date_joined} ({days_on_steam} dias na Steam) -Total de jogos: {total_games}.'
  payload = copy.deepcopy(payload_template)
  payload["contents"][0]["parts"][0]["text"] = prompt
  data = httpx.post(url, headers=headers, json=payload).json()
  return data['candidates'][0]['content']['parts'][0]['text']



def top5_response(username, top_5):
  prompt=f'Analise os hábitos de jogo de um usuário com base nesses dados da Steam e faça um comentario. Uma abordagem mais empática, como se fosse algum amigo te analisando de forma leve. Mas também pode fazer piadas. Exemplo: "FIFA e Rocket League no topo? Clássico. Te imagino jogando de fone, xingando juiz invisível, e dizendo só mais uma às 3h da manhã." "Com esse tanto de horas de jogo ja dava pra ter se formado em medicina". Maximo de 300 caracteres, não utilize # e nem emojis, não rir com hahaha, conte uma curiosidade das pessoas que jogam o jogo mais jogado dele. Cite um ponto forte dos jogadores daquele jogo. foque no jogo mais jogado. -Nome:{username} -Top 5 jogos mais jogados: ${formatted_top5Games(top_5)}'
  payload = copy.deepcopy(payload_template)
  payload["contents"][0]["parts"][0]["text"] = prompt
  data = httpx.post(url, headers=headers, json=payload).json()
  return data['candidates'][0]['content']['parts'][0]['text']
 
def ai_responses(username, date_joined, total_games, time_played, time_played_per_genre, time_played_per_category, top_5, days_on_steam):
  return {
    "steamHistory": steamHistory_response(username, date_joined, total_games, time_played, days_on_steam),
    "topGames": top5_response(username, top_5),
    "genreStats": genre_response(username, time_played_per_genre, total_games, top_5),
    "categoryStats": category_response(username, time_played_per_category)
  }