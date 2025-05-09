import { FC } from "react";

interface CardProps {
  infos: {
    Username: string;
    Avatar: string;
    Tittle: string;
    Punchline: string;
    Description: string;
    Stats: Array<{ label: string; value: number }>;
    Img: string;
  }
}

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

const Card: FC<CardProps> = ({ infos }) => {
  
  const user = {
    name: infos.Username,
    avatar: infos.Avatar,
  };

  const playerType = {
    title: infos.Tittle,
    punchline: infos.Punchline,
    description: infos.Description,
    stats: infos.Stats,
    img: infos.Img
  };

// const Card: FC = () => {
  return (
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
  );
};

export default Card;