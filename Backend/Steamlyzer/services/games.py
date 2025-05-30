# Importações necessárias para requisições HTTP assíncronas, manipulação de JSON e controle de execução assíncrona
import aiohttp, json, asyncio
from Steamlyzer.utils.constants import HEADERS, STEAM_API_KEY
from Steamlyzer.utils.retry import make_request_with_retry

# Função para buscar categorias e gêneros de um jogo na Steam Store
async def fetch_game_genres(session, game):
    appid = game["appid"]
    game_details_url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=en&cc=BR"

    try:
        # Faz requisição para obter os detalhes do jogo na loja da Steam
        async with session.get(game_details_url, headers=HEADERS) as resp:
            text_data = await resp.text()
            data = json.loads(text_data)

        # Se a resposta não for bem-sucedida, tenta novamente usando a lógica de retry
        if resp.status != 200:
            data = make_request_with_retry(game_details_url)
            if data is None:
                return {
                    "categories": "",
                    "genres": "",
                }

        # Extrai as categorias e gêneros do jogo (limitando a 6 de cada)
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
        # Em caso de erro, retorna categorias e gêneros vazios
        return {
            "categories": "",
            "genres": "",
        }

# Função que coleta detalhes sobre um jogo, incluindo conquistas e horas jogadas
async def fetch_details(session, game, steam_id, most_played_games):
    appid = game["appid"]
    game_name = game.get("name", "Jogo Desconhecido")
    game_image = game.get("img_icon_url", "")

    # URL para obter conquistas do jogador no jogo atual
    achievements_url = (
        f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
        f"?appid={appid}&key={STEAM_API_KEY}&steamid={steam_id}"
    )

    # URL da imagem do jogo
    image_url = f'https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{appid}/{game_image}.jpg'

    # Busca categorias e gêneros do jogo
    game_details = await fetch_game_genres(session, game)

    # Se o jogo estiver entre os mais jogados, busca também as conquistas
    if game in most_played_games:
        try:
            async with session.get(achievements_url) as resp:
                data = await resp.json()
                achievements = data.get("playerstats", {}).get("achievements", [])

                # Separa conquistas alcançadas e não alcançadas
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

                # Se o tempo jogado for muito baixo, ignora conquistas
                if int(game.get("playtime_forever")) <= 120:
                    return {
                        "game": game_name,
                        "image": image_url,
                        "appid": appid,
                        "total_achieved": 0,
                        "progress_achievements": 0,
                        "hours": 0,
                        "categories": [],
                        "genres": []
                    }

                # Retorna dados com progresso nas conquistas
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
            # Caso aconteça algum erro na obtenção de conquistas
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
        # Se o jogo tiver mais de 2h, pega categorias/genres mas ignora conquistas
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
            # Jogo pouco jogado, retorna dados mínimos
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

# Função que organiza a execução em lotes para buscar dados de todos os jogos de forma otimizada
async def gather_data_in_batches(games, steam_id, most_played_games):
    # Ordena os jogos por tempo jogado (descendente)
    games.sort(key=lambda game: game["playtime_forever"], reverse=True)

    # Conta quantos jogos têm pelo menos 2 horas jogadas
    qtd = sum(1 for jogo in games if jogo.get("playtime_forever", 0) >= 120)

    # Define o tamanho do lote e o tempo de espera com base na quantidade de jogos relevantes
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
        sleep_time = 1  # Pode ajustar conforme testes

    all_results = []

    # Cria uma sessão HTTP reutilizável para todos os lotes
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(games), batch_size):
            batch = games[i:i + batch_size]  # Define o grupo de jogos do lote atual
            tasks = [
                fetch_details(session, game, steam_id, most_played_games)
                for game in batch
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            all_results.extend(results)

            # Pausa entre os lotes para evitar bloqueio por excesso de requisições
            await asyncio.sleep(sleep_time)

    return all_results
