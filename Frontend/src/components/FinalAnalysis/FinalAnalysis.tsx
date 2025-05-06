import { FC, useEffect, useState } from "react";
import { motion } from "framer-motion";

//     "player type": {
//   "title": "O Craque",
//   "img": "/static/images/OCraque.png",
//   "description": "O Craque não é só talento, mas também disciplina, competitividade e a busca constante por evolução. Dentro do campo ou quadra, ele treina, refina habilidades e transforma a pressão em combustível para a vitória. Não importa o esporte, o objetivo é sempre dominar a dinâmica do jogo, antecipar movimentos e explorar cada oportunidade. Para ele, o sucesso vem tanto da técnica quanto da mentalidade forte, e cada partida é tratada com a seriedade de uma verdadeira disputa. A vitória não é só esperada, é construída lance a lance"
// },
interface FinalAnalysisProps {
  infos: {
    Username: string;
    playerTypeTittle: string;
    playerTypeImg: string;
    playerTypeDescription: string;
  }
}

const user = {
  name: "Biells",
  avatar: "https://avatars.steamstatic.com/eb351704cd4289bb74d811c051bca506da98f0df_full.jpg" // Troque para o avatar do usuário
};

const playerType = {
  title: "O Craque",
  punchline: "Até no tutorial ele bate no peito e pede o passe.",
  description: 'O Craque não é só talento, mas também disciplina, competitividade e a busca constante por evolução. Dentro do campo ou quadra, ele treina, refina habilidades e transforma a pressão em combustível para a vitória. Não importa o esporte, o objetivo é sempre dominar a dinâmica do jogo, antecipar movimentos e explorar cada oportunidade. Para ele, o sucesso vem tanto da técnica quanto da mentalidade forte, e cada partida é tratada com a seriedade de uma verdadeira disputa. A vitória não é só esperada, é construída lance a lance.',
  stats: [
    { label: "Força", value: 7 },
    { label: "Reflexo", value: 9 },
    { label: "Estratégia", value: 6 },
    { label: "Criatividade", value: 8 },
    { label: "Persistência", value: 7 },
    { label: "Carisma", value: 9 }
  ],
  img: "http://127.0.0.1:8000/static/images/PilotoDeAltaVelocidade.png" // Ícone do arquétipo
};
interface StatBarProps {
  label: string;
  value: number;
}

const StatBar = ({ label, value }: StatBarProps) => (
  <div className="flex items-center justify-between text-sm font-medium text-gray-200">
    <span className="w-24">{label}</span>
    <div className="flex-1 mx-2 h-2 bg-gray-700 rounded">
      <div
        className="h-full bg-amber-500 rounded hover:bg-amber-300"
        style={{ width: `${(value / 10) * 100}%` }}
      />
    </div>
    <span className="w-8 text-right">{value}/10</span>
  </div>
);


// const FinalAnalysis: FC<FinalAnalysisProps> = ({ infos }) => {
const FinalAnalysis: FC = () => {
  const [flipped, setFlipped] = useState(false);

  return (
    <div>
      <motion.div
        animate={{ rotateY: flipped ? 180 : 0 }}
        transition={{ duration: 0.8 }}
        style={{ transformStyle: 'preserve-3d' }}
      >
          <div className="flex justify-center rounded-2xl border-y-4 border-amber-500">
          {/* Card wrapper – fixed MTG‑like aspect with rounded borders */}
          <div className="relative w-[500px] aspect-[2/3] rounded-xl border-2 border-zinc-900 bg-zinc-900 ">
          
            {/* Top banner */}
            <div className="relative flex items-center justify-center px-5 py-3 bg-gradient-to-b from-zinc-900/90 to-zinc-900 rounded-t-xl">
              <img
                src={user.avatar}
                alt={user.name}
                className="absolute -top-6 left-4 h-16 w-16 rounded-full object-cover
                  ring-2 ring-amber-400 ring-offset-2 ring-offset-zinc-900
                  shadow-md transition-transform duration-300 hover:scale-105 z-20"
              />
              <div className="font-bold text-xl tracking-wide text-amber-100 hover:scale-105 hover:text-amber-500 duration-300">
              {user.name}
            </div>
            </div>

            {/* Artwork area */}
            <div className="relative h-[42%]">
              <img
                src={playerType.img}
                alt={playerType.title}
                className="object-cover h-full w-full"
              />

              {/* Title overlay */}
              <div className="absolute bottom-0 w-full bg-gradient-to-t from-black/90 to-transparent p-4">
                <h2 className="text-2xl font-extrabold text-gray-100 drop-shadow-md">
                  {playerType.title}
                </h2>
                <p className="italic text-sm text-amber-400">{playerType.punchline}</p>
              </div>
            </div>

            <div className="border-b-2 border-zinc-800  rounded-lg m-4 mt-3 mb-3">
              {/* Description */}
              <div className="px-4  text-gray-200 text-sm leading-relaxed prose prose-invert">
                <p className="text-justify text-gray-300 hover:text-white">{playerType.description}</p>
              </div>
              {/* Stats (optional) */}
              <div className="px-4 pt-2 pb-3 ">
                {playerType.stats.map((s) => (
                  <StatBar key={s.label} label={s.label} value={s.value} />
                ))}
              </div>

              {/* Bottom brand bar */}
              <div className=" relative top-2 flex items-center text-center justify-center text-[10px] text-gray-400 uppercase">
                <p className=" flex justify-center px-4 bg-zinc-900">
                  Steam Analyzer
                </p>
              </div>
            </div>

          </div>
        </div>
      </motion.div>
    </div>
  );

};

export default FinalAnalysis;