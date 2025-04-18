import { FC, useState, useEffect, useRef } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSteam } from '@fortawesome/free-brands-svg-icons'
import { Typewriter, SteamHistory, GenreStats, TopGames } from "@/components";
import axios from "axios";
import { faCircleQuestion } from '@fortawesome/free-solid-svg-icons'
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

// Componentes: SteamHistory, GenreStats, CategoryStats, TopGames, FinalAnalysis

const Home: FC = () => {
  const [steamData, setSteamData] = useState<any | null>(null);
  const analysisRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (steamData && analysisRef.current) {
      analysisRef.current.scrollIntoView({ behavior: "smooth" });
      console.log("Steam Data:", steamData)
    }
    if (formattedGenreInfo){
      console.log(`genre info:`, formattedGenreInfo)
    }
  }, [steamData]);

  async function fetchUserData(steamID: string) {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/steam/analyze/?steam_id=${steamID}`);
      setSteamData(response.data);
      console.log("Steam Data:", steamData)
    } catch (error) {
      console.error(error);
    }
  }

  const formattedSteamInfo = steamData ? {
    steam_id: steamData.info["steam_id"],
    Username: steamData.info["Username"],
    ProfileURL: steamData.info["Profile URL"],
    AvatarURL: steamData.info["Avatar URL"],
    DateJoined: steamData.info["Date Joined"],
    DaysOnSteam: steamData.info["Days on Steam"],
    totalGames: steamData.info["total games"],
    totalTimePlayed: steamData.info["total time played"]
  } : null;

  const formattedGenreInfo = steamData ? {
    Username: steamData.info["Username"],
    totalTimePlayed: steamData.info["total time played"],
    totalTimePlayedPerGenre: Object.entries(steamData.info["total time played per genre"]).map(([genre, time]) => ({
      genre,
      time: Number(time),
    })),
    totalGames: steamData.info["total games"],
    Top5MostPlayedGames: steamData.info["top 5 games"]
  } : null;

  const formattedTopGamesInfo = steamData ? {
    Username: steamData.info["Username"],
    totalGames: steamData.info["total games"],
    top5games: steamData.games.slice(0, 5)
  } : null;

  const { ref: inViewRef, inView } = useInView({
    triggerOnce: true, // Só anima na primeira vez que entrar na tela
    threshold: 0.2     // Só considera "visível" quando 20% do bloco aparece
  });

  return (
    <>
      <section>
        <div className="hero min-h-screen bg-base-200 items-start p-10">
          <div className="hero-content flex-col ">
            <div className="pt-8 w-full items-center justify-center flex-col flex">
              <Typewriter />
              <div className="relative mt-16 w-[600px]">
              <form onSubmit={(e) => { e.preventDefault(); fetchUserData((e.currentTarget[0] as HTMLInputElement).value) }} className="flex flex-col items-center">
                  <input
                    type="text"
                    className="peer w-full bg-transparent pl-10 text-slate-300 text-xl border border-slate-200 rounded-2xl px-3 py-2 transition-all duration-300 ease-in-out focus:outline-none hover:border-slate-500 shadow-sm focus:shadow"
                  />
                  <label className="pointer-events-none absolute ml-5 cursor-text bg-base-200 px-1 left-2.5 top-3 text-slate-400 text-sm transition-all transform origin-left peer-focus:-top-2 peer-focus:left-2.5 peer-focus:text-xs peer-focus:text-slate-400 peer-focus:scale-90">
                  Perfil Steam
                  </label>
                  <button
                    type="submit"
                    className="mt-4 bg-amber-500 text-black px-4 py-2 rounded-xl font-semibold transition-transform duration-300 hover:bg-amber-400 hover:scale-105 active:scale-95"
                  >
                    Analisar Perfil
                  </button>
                </form>
                <FontAwesomeIcon className="absolute left-2.5 top-3.5" icon={faSteam} />
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
            {formattedSteamInfo && formattedGenreInfo && formattedTopGamesInfo && (
              <div ref={analysisRef} className="w-full items-center justify-center flex-col flex">
                <motion.div
                  ref={inViewRef} // Aqui é onde conectamos o observer
                  className="w-full"
                  initial={{ opacity: 0, y: 20 }}
                  animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
                  transition={{ duration: 0.6, ease: 'easeOut' }}
                >
                  <SteamHistory info={formattedSteamInfo} />
                  <GenreStats infos={formattedGenreInfo} />
                  <TopGames info={formattedTopGamesInfo} />
                </motion.div>
              </div>
            )}
          </div>
        </div>
      </section>
    </>
  );
};

export default Home;
