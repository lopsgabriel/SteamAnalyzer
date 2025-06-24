import { FC, useState, useEffect, useRef } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSteam } from '@fortawesome/free-brands-svg-icons'
import { Typewriter, SteamHistory, GenreStats, TopGames, FinalAnalysis, MotionDiv, CategoryStats } from "@/components";
import axios from "axios";
import { faCircleQuestion } from '@fortawesome/free-solid-svg-icons';
import { TailSpin } from 'react-loader-spinner';

const Home: FC = () => {
  const [steamData, setSteamData] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const analysisRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (steamData && analysisRef.current) {
      analysisRef.current.scrollIntoView({ behavior: "smooth" });
      console.log(steamData)
    }
    if (steamData) {
      setErrorMessage(null);
      setLoading(false);
      console.table({
        formattedSteamInfo,
        formattedGenreInfo,
        formattedTopGamesInfo,
        formattedCategoryInfo,
        formattedFinalAnalysisInfo,
      });
      localStorage.setItem("steamAvatar", steamData.info["Avatar URL"]);
      localStorage.setItem("username", steamData.info["Username"]);
      localStorage.setItem("steamID", steamData.info["steam_id"]);
      localStorage.setItem("profileURL", steamData.info["Profile URL"]);
    }
    
  }, [steamData]);

  async function fetchUserData(steamID: string) {
    try {
      setErrorMessage(null);
      setLoading(true);
      const response = await axios.get(`https://steamanalyzer-production.up.railway.app/steam/analyze/?steam_id=${steamID}`);
      setSteamData(response.data);
    } catch (error: any) {
      setLoading(false);
      if (error.response?.status === 400 || error.response?.status === 429) {
        setErrorMessage(error.response?.data["error"]);
      } else {
        setErrorMessage("Oops! Algo deu errado, tente novamente.");
      }
    }
  }

  
  const formattedSteamInfo = steamData ? {
    DateJoined: steamData.info["Date Joined"],
    DaysOnSteam: steamData.info["Days on Steam"],
    totalGames: steamData.info["total games"],
    totalTimePlayed: steamData.info["total time played"],
    AImessage: steamData.AI_response['steamHistory']
  } : null;

  const top5games = steamData ? steamData.info["top 5 games"] : null
  const simplifiedGames = top5games
  ? top5games.map((game: any) => ({
      name: game.game,
      hours: game.hours
    }))
  : null;

  const formattedGenreInfo = steamData ? {
    totalTimePlayed: steamData.info["total time played"],
    totalTimePlayedPerGenre: Object.entries(steamData.info["total time played per genre"]).map(([genre, time]) => ({
      genre,
      time: Number(time),
    })),
    totalGames: steamData.info["total games"],
    shorterTop5Games: simplifiedGames,
    AImessage: steamData.AI_response['genreStats']
  } : null;

  const formattedTopGamesInfo = steamData ? {
    totalGames: steamData.info["total games"],
    top5games: steamData.info["top 5 games"],
    AImessage: steamData.AI_response['topGames']
  } : null;

  const formattedCategoryInfo = steamData ? {
    ChartData: Object.entries(steamData.info["total time played per category"]).map(
      ([name, hours]) => ({ name, hours: Number(hours) })
    ),
    AImessage: steamData.AI_response['categoryStats']
  } : null;

  const playerType = steamData ? steamData.info["player type"] : null;
  const formattedFinalAnalysisInfo = steamData ? {
    Tittle: playerType.title,
    Punchline: playerType.punchline,
    Description: playerType.description,
    Stats: playerType.stats.map((o: Record<string, number>) => {
      const [label, value] = Object.entries(o)[0];
      return { label, value };
    }),
    Img: playerType.img
  } : null;

  return (
    <>
      <section>
        <div className="hero min-h-screen bg-base-200 items-start p-10">
          <div className="hero-content flex-col ">
            <div className="pt-8 w-full items-center justify-center flex-col flex">
              <Typewriter />
              <div className="relative mt-16 w-[600px]">
                <p className="text-xs text-zinc-500 mb-3 pl-4">Certifique-se que seu perfil na Steam esteja público.</p>
              <form onSubmit={(e) => { e.preventDefault(); fetchUserData((e.currentTarget[0] as HTMLInputElement).value) }} className="flex flex-col items-center">
                  <input
                    spellCheck="false"
                    type="text"
                    className="peer w-full bg-transparent pl-10 text-slate-300 text-xl border border-slate-200 rounded-2xl px-3 py-2 transition-all duration-300 ease-in-out focus:outline-none hover:border-slate-500 shadow-sm focus:shadow"
                  />
                  <label className="pointer-events-none absolute ml-5 cursor-text bg-base-200 px-1 left-2.5 top-10 pr-80 text-slate-400 text-sm transition-all transform origin-left peer-focus:top-5 peer-focus:left-2.5 rounded-full peer-focus:text-xs peer-focus:text-slate-400 peer-focus:scale-90 peer-focus:pr-1">
                  Perfil Steam
                  </label>
                  <div className="flex items-center justify-center mt-4 duration-300">
                    {loading && <TailSpin color="white" height={40} width={40} />}
                    {errorMessage && <p className="text-red-500 text-sm">{errorMessage}</p>}
                  </div>
                  <button
                    type="submit"
                    className="mt-4 bg-amber-500 text-white px-4 py-2 rounded-xl font-medium transition-transform duration-300 hover:scale-105 active:scale-95"
                  >
                    Analisar Perfil
                  </button>
                </form>
                <FontAwesomeIcon className="absolute left-2.5 top-10 text-zinc-300" icon={faSteam} />
                <div className="flex flex-col pt-4 pl-4">
                  <p className="text-slate-400 font-sora">Voce pode usar:</p>
                  <div className="flex gap-6 pt-1">
                    <div className="flex items-center gap-2">
                      <span className="w-1 h-1 bg-slate-400 rounded-full"></span>
                      <span className="text-slate-300 text-xs">Steam ID</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="w-1 h-1 bg-slate-400 rounded-full"></span>
                      <span className="text-slate-300 text-xs">URL Personalizado</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="w-1 h-1 bg-slate-400 rounded-full"></span>
                      <span className="text-slate-300 text-xs">Link do Perfil</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="relative mt-4 py-4 w-full max-w-xl">
                <div className="flex flex-col border-[0.5px] hover:border-slate-500 rounded-xl duration-300 p-4 items-left justify-center">
                  <h2 className="bg-base-200 px-1 absolute text-slate-400 top-1 font-onest">Como encontrar?</h2>

                  <div className="flex items-start gap-2 mt-6">
                    <FontAwesomeIcon icon={faCircleQuestion} className="text-amber-400 mt-1" />
                    <p className="text-slate-400 font-onest">
                      <span className="text-slate-300 font-semibold">Steam ID:</span> Abra a Steam, clique no seu nome de usuário no canto superior direito, selecione "Detalhes da conta" e o seu ID Steam será exibido abaixo do seu nome de usuário.
                    </p>
                  </div>

                  <div className="flex items-start gap-2 mt-4">
                    <FontAwesomeIcon icon={faCircleQuestion} className="text-amber-400 mt-1" />
                    <p className="text-slate-400 font-onest">
                      <span className="text-slate-300 font-semibold">URL Personalizado:</span> Acesse o perfil da Steam, clique em "Editar perfil" e lá vai estar a URL personalizada.
                    </p>
                  </div>

                  <div className="flex items-start gap-2 mt-4">
                    <FontAwesomeIcon icon={faCircleQuestion} className="text-amber-400 mt-1" />
                    <p className="text-slate-400 font-onest">
                      <span className="text-slate-300 font-semibold">Link do Perfil:</span> Acesse o perfil da Steam, copie o link do perfil e cole aqui.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            {formattedSteamInfo && formattedGenreInfo && formattedTopGamesInfo && formattedCategoryInfo && formattedFinalAnalysisInfo && (
              <div ref={analysisRef} className="w-full items-center justify-center flex-col flex">
                <MotionDiv>
                  <SteamHistory info={formattedSteamInfo} />
                  <TopGames info={formattedTopGamesInfo} />
                  <GenreStats infos={formattedGenreInfo} />
                  <CategoryStats infos={formattedCategoryInfo} />
                  <FinalAnalysis infos={formattedFinalAnalysisInfo} />
                </MotionDiv>
              </div>
            )}
          </div>
        </div>
      </section>
    </>
  );
};

export default Home;
