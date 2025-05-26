import time
import aiohttp
from rest_framework.response import Response
from rest_framework import status
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
              return Response({"error": f"Erro ao buscar dados do perfil da Steam: {resp.status} - {error_message}"}, status=resp.status)

          data = await resp.json()
          if data['response']['players'][0]['communityvisibilitystate'] != 3:
              return Response({"error": "Hmm... Parece que seu perfil está privado! Torne-o público e tente novamente."}, status=status.HTTP_403_FORBIDDEN)
          return data
      
  except Exception as e:
      print(f"Erro ao buscar dados do perfil da Steam: {str(e)}")
      return {"error": f"Erro ao buscar dados do perfil da Steam: {str(e)}"}
  

async def gather_user_profile(steam_id):
    async with aiohttp.ClientSession() as session:
        profile_data = await fetch_user_profile(session, steam_id)
        return profile_data