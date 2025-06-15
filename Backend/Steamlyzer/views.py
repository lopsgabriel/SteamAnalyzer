"""ViewSets responsáveis pelas análises do perfil Steam."""

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
import asyncio
import aiohttp
import nest_asyncio
import requests
from collections import Counter
from setup.utils.player_type_logic import define_player_type
from Steamlyzer.services.games import gather_data_in_batches
from Steamlyzer.services.profile import gather_user_profile
from Steamlyzer.services.steam_api import verify_steamid_or_vanity_url
from Steamlyzer.services.ai_responses import ai_responses
from Steamlyzer.utils.retry import make_request_with_retry
from Steamlyzer.utils.constants import STEAM_API_KEY
nest_asyncio.apply()
class SteamAnalyzerViewSet(ViewSet):

    @action(detail=False, methods=["get"])
    def analyze(self, request):
        try:
            steam_id = request.query_params.get("steam_id")

            if not steam_id:
                return Response({"error": "Preencha o campo do usuario"}, status=400)
            
            steam_id = verify_steamid_or_vanity_url(steam_id)
            if not steam_id:
                return Response({"error": "Usuario não encontrado. Tente novamente."}, status=400)
            
            try:
                # Executa o async
                user_profile_data = asyncio.run(gather_user_profile(steam_id))
                if not isinstance(user_profile_data, dict):
                    print("user_profile_data inválido:", user_profile_data)
                    return Response({"error": "Erro ao obter perfil do usuário."}, status=500)

                user_data = user_profile_data.get("response", {}).get("players", [{}])[0]
            except Exception as e:
                print("Erro ao buscar dados da Steam:", e)
                return Response({"error": "Erro ao buscar dados da Steam 2"}, status=500)

            #busca jogos do usuario pela steamID          
            url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id}&include_appinfo=1&include_played_free_games=1"
            response = requests.get(url)

            #Antes quando o response fosse diferente de 200, e o retry desse erro, dava attributeerror: NoneType, corrigi com uma logica para identificar corretamente quando deu erro
            if response.status_code != 200:
                retried_response = make_request_with_retry(url)
                if retried_response is None or retried_response.status_code != 200:
                    print("Erro ao chamar API da Steam:", retried_response.status_code if retried_response else "None", 
                        retried_response.text if retried_response else "Sem resposta")
                    return Response({"error": "Erro ao buscar jogos da Steam"}, status=500)
                response = retried_response

        except Exception:
            return Response({"error": "Erro ao buscar dados da Steam"}, status=500)

        if response.status_code != 200:
            print("Erro ao chamar API da Steam:", response.status_code, response.text)
            return Response({"error": "Erro ao buscar jogos da Steam"}, status=500)
        data = response.json()

        games = data.get("response", {}).get("games", [])
        most_played_games = sorted(games, key=lambda x: x["playtime_forever"], reverse=True)[:10]
            
        genres_hours = {}
        categories_hours = {}

        timecreated = user_data.get("timecreated", 0)
        created_at = datetime.fromtimestamp(timecreated)

        now = datetime.now()
        delta = now - created_at
        days_since_creation = delta.days

        games_data = asyncio.run(gather_data_in_batches(games, steam_id, most_played_games))

        # Cria um dicionário com os dados dos jogos
        wanted = {
            "game": "Unknown",
            "image": "unknown",
            "appid": 0,
            "total_achieved": 0,
            "progress_achievements": [],
            "hours": 0,
        }
        shorter_games = [
            {k: g.get(k, default) for k, default in wanted.items()}
            for g in games_data
        ]

        # Filtra jogos com horas > 0, ordena, pega top‑5
        top_5_games = sorted(
            (g for g in shorter_games if g["hours"] > 0),
            key=lambda g: g["hours"],
            reverse=True
        )[:5]
        
        # Soma horas por gênero e categoria
        genres_hours = Counter()
        categories_hours = Counter()

        for g in games_data:
            genres_hours.update({genre: g["hours"] for genre in g.get("genres", [])})
            categories_hours.update({cat: g["hours"] for cat in g.get("categories", [])})

        genres_hours = dict(sorted(genres_hours.items(), key=lambda item: item[1], reverse=True)[:6])
        categories_hours = dict(sorted(categories_hours.items(), key=lambda item: item[1], reverse=True)[:6])
        player_type = define_player_type(genres_hours, categories_hours)
        time_played = round((sum(int(game["playtime_forever"]) for game in games if isinstance(game, dict) and "playtime_forever" in game) / 60), 2)
        ai_responses_data = ai_responses(
                user_data.get("personaname", "Unknown"), (created_at.strftime("%d-%m-%Y")), len(games), time_played, genres_hours, categories_hours, top_5_games, days_since_creation)
        result = {
            "info": {
                "steam_id": steam_id,
                "Username": user_data.get("personaname", "Unknown"),
                "Profile URL": f"https://steamcommunity.com/profiles/{steam_id}/",
                "Avatar URL": user_data.get("avatarfull", ""),
                "Date Joined": created_at.strftime("%d-%m-%Y"),
                "Days on Steam": days_since_creation,
                "Visibility State": user_data.get("communityvisibilitystate", ""),
                "total games": len(games),
                "total time played":  time_played,
                "total time played per genre": genres_hours,
                "total time played per category": categories_hours,
                "player type": player_type,
                "top 5 games": top_5_games
            },
            "AI_response": ai_responses_data
        }
        return Response(result)