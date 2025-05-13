import aiohttp, json, asyncio
from Steamlyzer.utils.constants import HEADERS, STEAM_API_KEY
from Steamlyzer.utils.retry import make_request_with_retry

async def fetch_game_genres(session, game):
    appid = game["appid"]
    print("mandando 1 request 6")
    game_details_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=en&cc=BR"

    try:
        async with session.get(game_details_url, headers=HEADERS) as resp:

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
                        "hours": 0,
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
                    "hours": round(int(game["playtime_forever"]) / 60),
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
                "hours": round(int(game["playtime_forever"]) / 60),
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
                "hours": round(int(game["playtime_forever"]) / 60),
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
                "hours": round(int(game["playtime_forever"]) / 60),
                "categories": [],
                "genres": []
            }
        

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
    