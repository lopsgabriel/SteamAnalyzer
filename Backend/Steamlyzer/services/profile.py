import aiohttp
import asyncio
from rest_framework.response import Response
from rest_framework import status
from Steamlyzer.utils.retry import make_request_with_retry
from Steamlyzer.utils.constants import STEAM_API_KEY
import requests

# Função assíncrona que busca os dados do perfil do usuário na API da Steam
async def fetch_user_profile(session, steam_id):
    try:
        # Monta a URL para a chamada da API GetPlayerSummaries
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id}"

        # Pequeno delay para evitar excesso de requisições (rate limiting)
        await asyncio.sleep(0.5)

        # Faz a requisição GET de forma assíncrona usando a sessão atual
        async with session.get(url) as resp:
            # Se a resposta não for 200 (OK), tenta uma nova requisição com a função de retry
            if resp.status != 200:
                data = make_request_with_retry(url)
                if data and isinstance(data, requests.Response):
                    if data.status_code == 429:
                        return Response({"error": "A API da Steam está limitando o número de requisições. Tente novamente em alguns segundos."},
                                        status=429)
                    try:
                        return data.json()
                    except Exception:
                        return Response({"error": "Resposta inesperada da API da Steam."}, status=500)

                # Caso ainda assim falhe, retorna o erro como texto na resposta
                error_message = await resp.text()
                return Response(
                    {"error": f"Erro ao buscar dados do perfil da Steam: {resp.status} - {error_message}"},
                    status=resp.status
                )

            # Converte a resposta da API para JSON
            data = await resp.json()

            # Verifica se o perfil está público (communityvisibilitystate = 3)
            if data['response']['players'][0]['communityvisibilitystate'] != 3:
                return Response(
                    {"error": "Hmm... Parece que seu perfil está privado! Torne-o público e tente novamente."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Tudo certo, retorna os dados do perfil
            return data

    # Captura qualquer exceção que ocorra e retorna como erro
    except Exception as e:
        return {"error": f"Erro ao buscar dados do perfil da Steam: {str(e)}"}

# Função que orquestra a criação de uma sessão HTTP e chama a função principal de busca de perfil
async def gather_user_profile(steam_id):
    # Cria uma sessão HTTP com aiohttp
    async with aiohttp.ClientSession() as session:
        # Chama a função de busca passando a sessão e o Steam ID
        profile_data = await fetch_user_profile(session, steam_id)
        return profile_data
