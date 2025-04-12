from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
import aiohttp
import asyncio
import os
import nest_asyncio
import requests

nest_asyncio.apply()

STEAM_API_KEY = str(os.getenv("STEAM_API_KEY"))


class SteamAnalyzerViewSet(ViewSet):

    @action(detail=False, methods=["get"])
    def analyze(self, request):
        steam_id = request.query_params.get("steam_id")

        if not steam_id:
            return Response({"error": "steam_id is required"}, status=400)

        url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id}&include_appinfo=1&include_played_free_games=1"

        # Continua usando requests aqui, pra manter o mínimo de mudanças
        response = requests.get(url)

        if response.status_code != 200:
            return Response({"error": "Erro ao buscar dados da Steam"}, status=500)

        data = response.json()
        games = data.get("response", {}).get("games", [])

        async def fetch_user_profile(session):
            try:
                url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={steam_id}"
                async with session.get(url) as resp:
                    data = await resp.json()
                    return data
            except Exception:
                return {"erro": "Erro ao buscar dados do perfil da Steam"}


        # Define a função async pra buscar a categoria e genero do jogo
        async def fetch_game_genres(session, game):
            appid = game["appid"]
            game_details_url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
            try:
              async with session.get(game_details_url) as resp:
                data = await resp.json()
                game_details = data.get(str(appid), {}).get("data", {})

                raw_categories = game_details.get("categories", [])
                raw_genres = game_details.get("genres", [])

                game_categories = [cat["description"] for cat in raw_categories]
                game_genres = [gen["description"] for gen in raw_genres]

                return {
                    "categories": game_categories[0:6],
                    "genres": game_genres[0:6]
                }
            except Exception:
                return {
                    "categories": "",
                    "genres": ""
                }

        # Define a função async pra buscar conquistas
        async def fetch_details(session, game):
            appid = game["appid"]
            game_name = game.get("name", "Jogo Desconhecido")
            achievements_url = (
                f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
                f"?appid={appid}&key={STEAM_API_KEY}&steamid={steam_id}"
            )
            try:
                async with session.get(achievements_url) as resp:
                    data = await resp.json()
                    achievements = data.get("playerstats", {}).get("achievements", [])
                    conquered = [
                        {
                            "apiname": ach["apiname"],
                            "unlocktime": ach["unlocktime"]
                        }
                        for ach in achievements if ach["achieved"] == 1
                    ]
                    not_conquered = [
                        ach for ach in achievements if ach["achieved"] == 0
                    ]
                    total_achievements = len(conquered) + len(not_conquered)

                    game_details = await fetch_game_genres(session, game)

                    if game.get("playtime_forever") <= 60:
                        return {
                          "game": game_name,
                          "progress_achievements": 0,
                          "time_played": 0,
                          "categories": [],
                          "genres": []
                        }
                    
                    return {
                      "game": game_name,
                      "total_achieved": total_achievements,
                      "progress_achievements": round((len(conquered) / total_achievements) * 100),
                      "time_played": round(int(game["playtime_forever"]) / 60),
                      "categories": game_details["categories"],
                      "genres": game_details["genres"]
                    }
                
            except Exception:
                return {
                  "game": game_name,
                  "total_achieved": 0,
                  "progress_achievements": 0,
                  "time_played": round(int(game["playtime_forever"]) / 60),
                  "categories": game_details["categories"],
                  "genres": game_details["genres"]
                }

        # Junta tudo em uma função assíncrona que será executada com asyncio.run
        async def gather_data():
            async with aiohttp.ClientSession() as session:
                tasks = [fetch_details(session, game) for game in games]
                return await asyncio.gather(*tasks)
        
        async def gather_user_profile():
            async with aiohttp.ClientSession() as session:
                profile_data = await fetch_user_profile(session)
                return profile_data
            
        genres_hours = {}
        categories_hours = {}

        user_profile_data = asyncio.run(gather_user_profile())
        user_data = user_profile_data.get("response", {}).get("players", [{}])[0]
        timecreated = user_data.get("timecreated", 0)
        created_at = datetime.fromtimestamp(timecreated)
        now = datetime.now()
        delta = now - created_at
        days_since_creation = delta.days

        games_data = asyncio.run(gather_data())
        shorter_games_data = []
        for game_data in games_data:
            shorter_games_data.append({
            "game": game_data.get("game", "Unknown"),
            "total_achieved": game_data.get("total_achieved", 0),
            "progress_achievements": game_data.get("progress_achievements", []),
            "time_played": game_data.get("time_played", 0),
        })
            
        even_shorter_games_data = (game for game in shorter_games_data if game["time_played"] > 0) 
        even_shorter_games_data = list(even_shorter_games_data)
        even_shorter_games_data.sort(key=lambda game: game["time_played"], reverse=True)

        for game in games_data:
            for genre in game["genres"]:
                if genre in genres_hours:
                    genres_hours[genre] += game["time_played"]
                else:
                    genres_hours[genre] = game["time_played"]
            for category in game["categories"]: 
                if category in categories_hours:
                    categories_hours[category] += game["time_played"]
                else:
                    categories_hours[category] = game["time_played"]
        
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
                "total time played": sum(int(game["playtime_forever"]) for game in games if isinstance(game, dict) and "playtime_forever" in game) / 60,
                "total time played per genre": dict(sorted(genres_hours.items(), key=lambda item: item[1], reverse=True)[:8]),
                "total time played per category": dict(sorted(categories_hours.items(), key=lambda item: item[1], reverse=True)[:8]),
              
            },
            "games": even_shorter_games_data,
        }
        return Response(result)
