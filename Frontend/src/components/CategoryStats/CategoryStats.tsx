import { FC, useState, useEffect } from "react";
import ChartSection from "./ui/ChartSection";
import { RiInformationLine } from "react-icons/ri";
import MotionDiv from "../MotionDiv/MotionDiv";
import axios from "axios";

interface CategoryStatsProps {
  infos: {
    Username: string;
    ChartData: Array<{ name: string; hours: number }>;
  };
}


const CategoryStats: FC<CategoryStatsProps> = ({ infos }) => {
  const [AIMessage, setAIMessage] = useState('');
  const chartData = infos.ChartData

  const geminiKey = 'AIzaSyDr7m5RBBPpjJHCILFXx2DVu5deQr-HW4s'
  const prompt = `
  Você é uma IA que analisa perfis de jogadores da Steam com base em estatísticas de tempo de jogo por categoria. Seu papel é gerar uma frase interpretativa e levemente descontraída sobre o estilo de jogo da pessoa com base nas categorias mais jogadas.
  Aqui estão os dados do jogador (em horas):

  - Nome: ${infos.Username}
  - Top 5 jogos mais jogados: ${infos.ChartData.map((g) => `${g.name}: ${g.hours.toFixed(2)}h`).join(', ')}

  Gere uma frase curta (1 ou 2 linhas), **sem sarcasmo**, apenas com uma leitura leve, humana e interpretativa sobre o perfil de jogo da pessoa. Não cite o nome do jogador e fale como se estivesse falando diretamente com ele utilizando "você". Leve em consideração a categoria mais jogada. Exemplo de tom desejado:

  > “Você tem um perfil bem equilibrado entre jogos solo e multiplayer. Provavelmente curte tanto explorar sozinho quanto competir ou cooperar com amigos.”

  Agora gere uma nova frase baseada nas estatísticas acima. Maximo de 250 caracteres`;


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