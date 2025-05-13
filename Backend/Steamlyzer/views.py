from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
import asyncio
import aiohttp
import nest_asyncio
import requests
from setup.utils.player_type_logic import define_player_type
from Steamlyzer.services.games import gather_data_in_batches, fetch_details
from Steamlyzer.services.profile import fetch_user_profile
from Steamlyzer.services.steam_api import verify_steamid_or_vanity_url
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
            
            print("mandando 1 request 3")
            #busca jogos do usuario pela steamID          
            url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id}&include_appinfo=1&include_played_free_games=1"
            response = requests.get(url)

            if response.status_code != 200:
                response = make_request_with_retry(url)
                print("Erro ao chamar API da Steam:", response.status_code, response.text)

        except Exception:
            return Response({"error": "Erro ao buscar dados da Steam"}, status=500)

        if response.status_code != 200:
            print("Erro ao chamar API da Steam:", response.status_code, response.text)
            return Response({"error": "Erro ao buscar jogos da Steam"}, status=500)
        data = response.json()

        games = data.get("response", {}).get("games", [])
        most_played_games = sorted(games, key=lambda x: x["playtime_forever"], reverse=True)[:10]
        print(most_played_games)

        
        async def gather_user_profile():
            async with aiohttp.ClientSession() as session:
                profile_data = await fetch_user_profile(session, steam_id)
                return profile_data
            
        genres_hours = {}
        categories_hours = {}

        user_profile_data = asyncio.run(gather_user_profile())
        print("🧠 Dados do perfil retornado:", user_profile_data)
        user_data = user_profile_data.get("response", {}).get("players", [{}])[0]

        timecreated = user_data.get("timecreated", 0)
        created_at = datetime.fromtimestamp(timecreated)

        now = datetime.now()
        delta = now - created_at
        days_since_creation = delta.days

        games_data = asyncio.run(gather_data_in_batches(games, steam_id, most_played_games))
        shorter_games_data = []
        for game_data in games_data:
            shorter_games_data.append({
            "game": game_data.get("game", "Unknown"),
            "image": game_data.get("image", " unknown"),
            "appid": game_data.get("appid", 0),
            "total_achieved": game_data.get("total_achieved", 0),
            "progress_achievements": game_data.get("progress_achievements", []),
            "hours": game_data.get("hours", 0),
        })
            
        even_shorter_games_data = (game for game in shorter_games_data if game["hours"] > 0) 
        even_shorter_games_data = list(even_shorter_games_data)
        even_shorter_games_data.sort(key=lambda game: game["hours"], reverse=True)
        top_5_games = even_shorter_games_data[:5]

        for game in games_data:
            for genre in game["genres"]:
                if genre in genres_hours:
                    genres_hours[genre] += game["hours"]
                else:
                    genres_hours[genre] = game["hours"]
            for category in game["categories"]: 
                if category in categories_hours:
                    categories_hours[category] += game["hours"]
                else:
                    categories_hours[category] = game["hours"]

        genres_hours = dict(sorted(genres_hours.items(), key=lambda item: item[1], reverse=True)[:6])
        categories_hours = dict(sorted(categories_hours.items(), key=lambda item: item[1], reverse=True)[:6])
        player_type = define_player_type(genres_hours, categories_hours)
        
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
                "total time played":  round((sum(int(game["playtime_forever"]) for game in games if isinstance(game, dict) and "playtime_forever" in game) / 60), 2),
                "total time played per genre": genres_hours,
                "total time played per category": categories_hours,
                "player type": player_type,
                "top 5 games": top_5_games
            }
        }
        return Response(result)