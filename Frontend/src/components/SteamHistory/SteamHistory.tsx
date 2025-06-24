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
    <div className="section-container mt-10">
      <img
        src={user.avatar ?? ''}
        alt={`${user.Username ?? ''}'s avatar`}
        className="w-24 h-24 rounded-full hover:scale-110 duration-300" 
      />
      <a href={user.profileURL ?? ''} target="_blank" className="section-title">
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
      <p className="section-message mx-4 whitespace-pre-wrap break-words max-h-48 overflow-y-auto">
        {AImessage}
      </p>
    </div>
  )

}
export default SteamHistory