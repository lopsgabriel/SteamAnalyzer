import { FC } from "react";
import axios from "axios";
import { useEffect, useState } from "react";
import { CalendarDays, Gamepad2, Clock, Hourglass } from 'lucide-react';


interface SteamHistoryProps {
  info: {
    steam_id: string;
    Username: string;
    ProfileURL: string;
    AvatarURL: string;
    DateJoined: string; // formato: "DD-MM-YYYY"
    DaysOnSteam: number;
    totalGames: number;
    totalTimePlayed: number; // em horas
  }
}

const SteamHistory: FC<SteamHistoryProps> = ({ info }) => {
  const { Username, ProfileURL, AvatarURL, DaysOnSteam, totalGames, totalTimePlayed } = info;
  const [AIMessage, setAIMessage] = useState('');
  const yearsOnSteam = (Number(DaysOnSteam) / 365).toFixed(1); 
  const geminiKey = 'AIzaSyDr7m5RBBPpjJHCILFXx2DVu5deQr-HW4s'

  const prompt = `
  Analise os hábitos de jogo de um usuário com base nesses dados da Steam e gere uma mensagem sarcástica,
   humilhe o jogador e deboche do jogador, não tenha pena, fale como alguem jovem:

  - Nome: ${info.Username}
  - Total de horas jogadas: ${info.totalTimePlayed.toFixed(2)}h
  - Conta criada em: ${info.DateJoined} (${info.DaysOnSteam} dias na Steam)
  - Total de jogos: ${info.totalGames}

  Seja engraçado, sarcástico, e ligeiramente crítico com o jogador, pode humilhar mesmoo, seja direta e curta, não utilize hashtags, não usar #, maximo de 250 caracteres.
  `;

  useEffect(() => {
    const fetchData = async () => {
      const message = await gerarMensagemDaIA(prompt);

      setAIMessage(message.candidates[0].content.parts[0].text);
    };
    fetchData();
    
  }, []);

  async function gerarMensagemDaIA(prompt: string) {
    try {
      const response = await axios.post(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${geminiKey}`,
        {
          contents: [{
              parts: [{ text: prompt }]
            }]
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Erro ao gerar resposta da IA:', error);
      return 'Erro ao gerar mensagem da IA.';
    }
  }

  return (
    <div className="bg-zinc-900 text-white p-6 rounded-2xl border-b-4 hover:shadow-zinc-900 mt-10 duration-300 border-amber-500 shadow-lg flex flex-col items-center gap-3 w-full max-w-2xl mx-auto">
      <img
        src={AvatarURL}
        alt={`${Username}'s avatar`}
        className="w-24 h-24 rounded-full hover:scale-110 duration-300" 
      />
      <a href={ProfileURL} target="_blank" className="text-2xl font-bold  hover:text-amber-400 transition-colors">
        {Username}
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
        {AIMessage || "Carregando..."}
      </p>
    </div>
  )

}
export default SteamHistory