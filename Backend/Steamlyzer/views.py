from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
import aiohttp
import asyncio
import os
import nest_asyncio
import requests
import re
import time
import json


semaphore = asyncio.Semaphore(5)

nest_asyncio.apply()

STEAM_API_KEY = str(os.getenv("STEAM_API_KEY"))

headers = {
            'Accept-Language': 'en-US,en;q=0.9'  # força o idioma pra inglês por padrão
        }

def make_request_with_retry(url):
    retries = 5
    delay = 1  # Delay inicial de 1 segundo
    for i in range(retries):
        print(f"Tentando novamente ({i+1}/{retries})... em {url}")
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        time.sleep(delay)
        delay *= 2  # Exponencia o tempo de espera
    return None

def resolve_vanity_url(custom_url):
    print("mandando 1 request 1")
    resolve_url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={STEAM_API_KEY}&vanityurl={custom_url}"
    response = requests.get(resolve_url)
    data = response.json()

    if data["response"]["success"] == 1:
        return data["response"]["steamid"]
    return None

def verify_steamid_or_vanity_url(steam_id):

    # verifica se é uma url completa com o id64
    match_profiles = re.search(r"steamcommunity\.com/profiles/(\d+)", steam_id)
    if match_profiles:
        return match_profiles.group(1)
    
    #verifica se é um vanity url e retorna o steam id64
    match_id = re.search(r"steamcommunity\.com/id/([\w-]+)", steam_id)
    if match_id:
        custom_url = match_id.group(1)
        print("mandando 1 request 2")
        resolve_url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={STEAM_API_KEY}&vanityurl={custom_url}"
        response = requests.get(resolve_url)
        data = response.json()

        if response.status_code != 200:
            data =make_request_with_retry(resolve_url)
            print("Erro ao chamar API da Steam:", response.status_code, response.text)


        if data["response"]["success"] == 1:
            print(data["response"]["steamid"])
            return data["response"]["steamid"]
        else:
            return None
    #verifica se é o id64 direto
    if re.fullmatch(r"\d{17}", steam_id):
        return steam_id
    
    if re.fullmatch(r"[\w-]+", steam_id):
        return resolve_vanity_url(steam_id)
    
    return None

async def fetch_game_genres(session, game):
    appid = game["appid"]
    print("mandando 1 request 6")
    game_details_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=en&cc=BR"


    try:
        async with session.get(game_details_url, headers=headers) as resp:

            print(f"Status da resposta: {resp.status}")
            print(f"Content-Type: {resp.headers.get('Content-Type')}")
            text_data = await resp.text()
            print("Texto da resposta:", text_data[:300])  # só os 300 primeiros chars pra não lotar o terminal

            data = json.loads(text_data)


        if resp.status != 200:
            print('vai tentar dnv')
            data = make_request_with_retry(game_details_url)
            if data == None:
                return {
                    "categories": "",
                    "genres": "",
                }
            print("Erro ao chamar API da Steam:", resp.status, resp.text)


        game_details = data.get(str(appid), {}).get("data", {})

        raw_categories = game_details.get("categories", [])
        raw_genres = game_details.get("genres", [])
        
        game_categories = [cat["description"] for cat in raw_categories]
        game_genres = [gen["description"] for gen in raw_genres]
        return {
            "categories": game_categories[0:6],
            "genres": game_genres[0:6],
        }
    except Exception:
        return {
            "categories": "",
            "genres": "",
        }
    

    
# Define a função async pra buscar conquistas
async def fetch_details(session, game, steam_id, most_played_games):

    appid = game["appid"]

    game_name = game.get("name", "Jogo Desconhecido")

    game_image = game.get("img_icon_url", "")

    achievements_url = (
        f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
        f"?appid={appid}&key={STEAM_API_KEY}&steamid={steam_id}"
    )

    image_url = f'https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{appid}/{game_image}.jpg'

    if game in most_played_games:
        try:
            print("mandando 1 request 5")
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



                if int(game.get("playtime_forever")) <= 120:
                    return {
                        "game": game_name,
                        "image": image_url,
                        "appid": appid,
                        "progress_achievements": 0,
                        "time_played": 0,
                        "categories": [],
                        "genres": []
                    }      
                
                game_details = await fetch_game_genres(session, game)

                return {
                    "game": game_name,
                    "image": image_url,
                    "appid": appid,
                    "total_achieved": total_achievements,
                    "progress_achievements": round((len(conquered) / total_achievements) * 100),
                    "time_played": round(int(game["playtime_forever"]) / 60),
                    "categories": game_details["categories"],
                    "genres": game_details["genres"]
                }
            
        except Exception:
            return {
                "game": game_name,
                "image": image_url,
                "appid": appid,
                "total_achieved": 0,
                "progress_achievements": 0,
                "time_played": round(int(game["playtime_forever"]) / 60),
                "categories": game_details["categories"],
                "genres": game_details["genres"]
            }
    else:
        if int(game.get("playtime_forever")) >= 120:
            game_details = await fetch_game_genres(session, game)
            return {
                "game": game_name,
                "image": image_url,
                "appid": appid,
                "total_achieved": 0,
                "progress_achievements": 0,
                "time_played": round(int(game["playtime_forever"]) / 60),
                "categories": game_details["categories"],
                "genres": game_details["genres"]
            }
        else:
            return {
                "game": game_name,
                "image": image_url,
                "appid": appid,
                "total_achieved": 0,
                "progress_achievements": 0,
                "time_played": round(int(game["playtime_forever"]) / 60),
                "categories": [],
                "genres": []
            }
    

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
                return {"erro": f"Erro ao buscar dados do perfil da Steam: {resp.status} - {error_message}"}

            data = await resp.json()
            return data
        
    except Exception as e:
        print(f"Erro ao buscar dados do perfil da Steam: {str(e)}")
        return {"erro": f"Erro ao buscar dados do perfil da Steam: {str(e)}"}
    
class SteamAnalyzerViewSet(ViewSet):

    @action(detail=False, methods=["get"])
    def analyze(self, request):
        try:
            steam_id = request.query_params.get("steam_id")

            if not steam_id:
                return Response({"error": "steam_id is required"}, status=400)
            
            steam_id = verify_steamid_or_vanity_url(steam_id)
            if not steam_id:
                return Response({"error": "steam_id is invalid"}, status=400)
            
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

        # Junta tudo em uma função assíncrona que será executada com asyncio.run
        async def gather_data_in_batches(games, steam_id, most_played_games):
            games.sort(key=lambda game: game["playtime_forever"], reverse=True)
            qtd = sum(1 for jogo in games if jogo.get("playtime_forever", 0) >= 120)

            print(qtd)
            if qtd >= 310:
                batch_size = 10
                sleep_time = 3
            elif qtd >= 170:
                batch_size = 20
                sleep_time = 3
            elif qtd >= 60:
                batch_size = 25
                sleep_time = 2
            else:
                batch_size = 30
                sleep_time = 1 # pode ajustar conforme testes  # pode ajustar conforme testes
            all_results = []

            async with aiohttp.ClientSession() as session:
                for i in range(0, len(games), batch_size):
                    print(f"Processando jogos {i} até {min(i + batch_size, len(games))}")
                    batch = games[i:i + batch_size]

                    tasks = [
                        fetch_details(session, game, steam_id, most_played_games)
                        for game in batch
                    ]
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    all_results.extend(results)

                    await asyncio.sleep(sleep_time)  # pausa entre os batches

            return all_results

        
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
            "time_played": game_data.get("time_played", 0),
        })
            
        even_shorter_games_data = (game for game in shorter_games_data if game["time_played"] > 0) 
        even_shorter_games_data = list(even_shorter_games_data)
        even_shorter_games_data.sort(key=lambda game: game["time_played"], reverse=True)
        top_5_games = [{
            'name': game["game"],
            "hours": game["time_played"],
        } for game in even_shorter_games_data[:5]]

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
                "total time played per genre": dict(sorted(genres_hours.items(), key=lambda item: item[1], reverse=True)[:6]),
                "total time played per category": dict(sorted(categories_hours.items(), key=lambda item: item[1], reverse=True)[:6]),
                # top 5 jogos informando apenas o nome e a quantidade de horas jogadas
                "top 5 games": top_5_games
                
            },
            "games": even_shorter_games_data,
        }
        return Response(result)
