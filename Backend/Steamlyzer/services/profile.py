import time
import requests
from Steamlyzer.utils.retry import make_request_with_retry
from Steamlyzer.utils.constants import STEAM_API_KEY

async def fetch_user_profile(session, steam_id):
  try:
      print("mandando 1 request 4")
      url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id}"
      time.sleep(0.5)

      async with session.get(url) as resp:

          if resp.status != 200:  # Corrigido aqui
              data = make_request_with_retry(url)
              if data:
                  return data
              print(f"Erro ao chamar API da Steam: {resp.status}")
              error_message = await resp.text()  # Pega a resposta em texto
              print(f"Mensagem de erro: {error_message}")
              return {"error": f"Erro ao buscar dados do perfil da Steam: {resp.status} - {error_message}"}

          data = await resp.json()
          return data
      
  except Exception as e:
      print(f"Erro ao buscar dados do perfil da Steam: {str(e)}")
      return {"error": f"Erro ao buscar dados do perfil da Steam: {str(e)}"}