import { FC, useState, useEffect } from "react";
import ChartSection from "./ui/ChartSection";
import { RiInformationLine } from "react-icons/ri";
import MotionDiv from "../MotionDiv/MotionDiv";
import axios from "axios";

interface CategoryStatsProps {
  infos: {
    ChartData: Array<{ name: string; hours: number }>;
  };
}


const CategoryStats: FC<CategoryStatsProps> = ({ infos }) => {
  const username = localStorage.getItem('username');
  const [AIMessage, setAIMessage] = useState('');
  const chartData = infos.ChartData

  const geminiKey = 'AIzaSyDr7m5RBBPpjJHCILFXx2DVu5deQr-HW4s'
  const prompt = `
    Analise os hábitos de jogo de um usuário com base nesses dados da Steam e faça um comentario. Uma abordagem mais empática, como se fosse algum amigo te analisando de forma leve. Mas também pode fazer piadas.
      Exemplo:
    "FIFA e Rocket League no topo? Clássico. Te imagino jogando de fone, xingando juiz invisível, e dizendo só mais uma às 3h da manhã."
    "Com esse tanto de horas de jogo ja dava pra ter se formado em medicina".
      Maximo de 300 caracteres, não utilize # e nem emojis, não rir com hahaha, foque na categoria mais jogada, conte uma curiosidade comportamental dos players que jogam a categoria mais jogada dele.

    - Nome: ${username}
    - Top 5 categorias mais jogadas: ${infos.ChartData.map((g) => `${g.name}: ${g.hours.toFixed(2)}h`).join(', ')}`
  ;


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
    <div className="bg-zinc-900 text-white p-6 rounded-2xl border-b-4 hover:shadow-zinc-900 mt-20 duration-300 border-amber-500 shadow-lg flex flex-col items-center gap-3 w-full max-w-2xl mx-auto">
      <MotionDiv>
        <div className="bg-zinc-900 text-white rounded-2xl duration-300 flex flex-col items-center w-full max-w-2xl mx-auto">
          <h1 className="text-2xl font-bold  hover:text-amber-400 transition-colors">Categorias Mais Jogadas</h1>
          <ChartSection chartData={chartData} />
          <p className="mt-4 italic text-center text-gray-300 border-t border-gray-700 hover:border-gray-500 pt-4 px-4 duration-300">
            {AIMessage || "Carregando..."}
          </p>
          <div className="w-full flex pt-4 px-4 ">
            <RiInformationLine className="w-4 h-4 text-gray-400 flex-none"/>
            <p className="mx-2 italic text-gray-400 hover:text-gray-300 duration-300 text-sm">
              {`O gráfico mostra as categorias mais jogadas em horas, um jogo é possivel conter diversas categorias ao mesmo tempo, inclusive Single-player e Multi-player simultaneamente.` }
            </p>
          </div>
        </div>
    </MotionDiv>
      </div>
  );
};

export default CategoryStats;