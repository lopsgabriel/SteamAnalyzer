import { FC, useEffect, useState } from "react";
import LayoutShell from "./ui/LayoutShell";
import Podium  from "./ui/Podium";
import GamesList from "./ui/GamesList";
import axios from "axios";
import './ui/Styles.css'
import MotionDiv from "../MotionDiv/MotionDiv";


interface game {
  game:string,
  image: string
  appid: number
  progress_achievements: number
  hours: number
  total_achieved: number
}

interface TopGamesProps {
  info:{
    Username: string,
    totalGames: number,
    top5games: Array<game>
  }
}

export interface GameProps {
  id: string
  name: string
  avatar: string
  place: number
  hours: number
}


const TopGames: FC<TopGamesProps> = ({info}) => {
  const podiumData = info.top5games.map((game, index) => ({
    id: game.appid.toString(),
    name: game.game,
    avatar: game.image,
    rank: index + 1,
    hours: game.hours 
  }))
  const geminiKey = 'AIzaSyDr7m5RBBPpjJHCILFXx2DVu5deQr-HW4s'
   const [AIMessage, setAIMessage] = useState('');

   const prompt = `
  Analise os hábitos de jogo de um usuário com base nesses dados da Steam e gere uma mensagem sarcástica,
   humilhe o jogador e deboche do jogador, não tenha pena, fale como alguem jovem, use memes e girias:

  - Nome: ${info.Username}
  - Top 5 jogos mais jogados: ${info.top5games.map((g) => `${g.game}: ${g.hours.toFixed(2)}h`).join(', ')}


  Seja debochado, sarcástico, e ligeiramente crítico com o jogador, pode humilhar mesmoo, seja direta e curta, maximo de 500 caracteres, não use hashtags, não comente o nome do jogador, maximo de 500 caracteres
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

  const Games = [...podiumData]
    .sort((a, b) => a.rank! - b.rank!)
    .map((GameProps, place) => ({ ...GameProps, place }))

  return(
    <MotionDiv>
      <LayoutShell AIMessage={AIMessage}>
        <Podium Games={Games} />
        <GamesList Games={Games} />
      </LayoutShell>
    </MotionDiv>
  )
}

export default TopGames