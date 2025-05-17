import { FC } from "react";
import { CalendarDays, Gamepad2, Clock, Hourglass } from 'lucide-react';


interface SteamHistoryProps {
  info: {
    DateJoined: string; // formato: "DD-MM-YYYY"
    DaysOnSteam: number;
    totalGames: number;
    totalTimePlayed: number; // em horas
    AImessage: string;
  }
}

const SteamHistory: FC<SteamHistoryProps> = ({ info }) => {
  const user = {
    Username: localStorage.getItem('username'),
    avatar: localStorage.getItem('steamAvatar'),
    steamID: localStorage.getItem('steamID'),
    profileURL: localStorage.getItem('profileURL'),
  }
  const {DaysOnSteam, totalGames, totalTimePlayed } = info;
  const yearsOnSteam = (Number(DaysOnSteam) / 365).toFixed(1); 
  const AImessage = info.AImessage

  return (
    <div className="bg-zinc-900 text-white p-6 rounded-2xl border-b-4 hover:shadow-zinc-900 mt-10 duration-300 border-amber-500 shadow-lg flex flex-col items-center gap-3 w-full max-w-2xl mx-auto">
      <img
        src={user.avatar ?? ''}
        alt={`${user.Username ?? ''}'s avatar`}
        className="w-24 h-24 rounded-full hover:scale-110 duration-300" 
      />
      <a href={user.profileURL ?? ''} target="_blank" className="text-2xl font-bold  hover:text-amber-400 transition-colors">
        {user.Username}
      </a>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-2 text-sm text-center w-full">
        <div className="bg-zinc-800 p-3 rounded-xl flex flex-col justify-center items-center hover:scale-110 duration-300">
          <CalendarDays size={20} className="text-gray-500 mb-1" />
          <p className="text-amber-400 font-bold">{DaysOnSteam}</p>
          <p className="text-gray-400">Dias</p>
        </div>
        <div className="bg-zinc-800 p-3 rounded-xl flex flex-col justify-center items-center hover:scale-110 duration-300">
          <Hourglass size={20} className="text-gray-500 mb-1" />
          <p className="text-amber-400 font-bold">{yearsOnSteam} </p>
          <p className="text-gray-400">Anos</p>
        </div>
        <div className="bg-zinc-800 p-3 rounded-xl flex flex-col justify-center items-center hover:scale-110 duration-300">
          <Gamepad2 size={20} className="text-gray-500 mb-1" />
          <p className="text-amber-400 font-bold">{totalGames}</p>
          <p className="text-gray-400">Jogos</p>
        </div>
        <div className="bg-zinc-800 p-3 rounded-xl flex flex-col justify-center items-center hover:scale-110 duration-300">
          <Clock size={20} className="text-gray-500 mb-1" />    
          <p className="text-amber-400 font-bold">{totalTimePlayed.toFixed(0)}</p>
          <p className="text-gray-400">Horas </p>
        </div>
      </div>
      <p className="mt-4 mx-4 italic text-center text-gray-300 border-t border-gray-700 hover:border-gray-500 duration-300 pt-4 px-4 whitespace-pre-wrap break-words max-h-48 overflow-y-auto">
        {AImessage}
      </p>
    </div>
  )

}
export default SteamHistory