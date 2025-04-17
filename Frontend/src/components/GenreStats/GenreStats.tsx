import { FC, useEffect, useState } from "react";
import ApexCharts, { ApexOptions } from "apexcharts";
import axios from "axios";
interface GenreStatsProps {
  infos: {
    Username: string;
    totalTimePlayed: number;
    totalTimePlayedPerGenre: Array<{ genre: string; time: number }>;
    totalGames: number;
    Top5MostPlayedGames: Array<{ name: string; hours: number }>;
  };
}

const GenreStats: FC<GenreStatsProps> = ({ infos }) => {
  const [AIMessage, setAIMessage] = useState('');
  const geminiKey = 'AIzaSyDr7m5RBBPpjJHCILFXx2DVu5deQr-HW4s'
    const prompt = `
    Analise os hábitos de jogo de um usuário com base nesses dados da Steam e gere uma mensagem sarcástica, humilhe o jogador e debochando do jogador, não tenha pena:
  
    - Usuario: ${infos.Username}
    - Total de jogos: ${infos.totalGames}
    - Tempo jogado em cada genero: ${infos.totalTimePlayedPerGenre.map((g) => `${g.genre}: ${g.time.toFixed(2)}h`).join(', ')}
    - Top 5 jogos mais jogados: ${infos.Top5MostPlayedGames.map((g) => `${g.name}: ${g.hours.toFixed(2)}h`).join(', ')}
 
  
    Seja debochado, sarcástico, e ligeiramente crítico com o jogador, pode brincar com as informações, seja curta, n é necessario comentar sobre todos os generos, mas faça o usuario dar uma risada ao ler sua resposta, comente pouco sobre os jogos, mas foque mais nos generos, comece a resposta com dizendo ao usuario que tipo de player ele é, seja curta e faça uma resposa pequena, maximo de 500 caracteres.
    `;


  useEffect(() => {
    // const total = infos.totalTimePlayed;
    const genres = infos.totalTimePlayedPerGenre.map((g) => g.genre);
    // const percentages = infos.totalTimePlayedPerGenre.map((g) =>
    //   total ? Math.round((g.time / total) * 100) : 0
    // );
    const percentages2 = infos.totalTimePlayedPerGenre.map((g) =>
    g.time)

    const fetchData = async () => {
      const message = await gerarMensagemDaIA(prompt);
      console.log(percentages2)

      setAIMessage(message.candidates[0].content.parts[0].text);
    };
    fetchData();

    const el = document.getElementById("pie-chart");
    if (!el) return;
    console.log("Elemento pie-chart existe?", el);

    const chartConfig: ApexOptions = {
      series: percentages2,
      chart: {
        type: "pie",
        width: 420,
        height: 420,
        toolbar: {
          show: false,
        },
      },
      title: {
        text: 'Horas por genero de jogo',
        align: "center",
        style: {
          fontSize: "16px",
          color: "#ffffff",
        },
      },
      stroke: {
        show: false,
      },
      dataLabels: {
        enabled: true,
        formatter: function (_val, opts) {
          return opts.w.globals.series[opts.seriesIndex];
        },
        style: {
          fontSize: "12px",
          colors: ["#ffffff"],
        },
      },
      colors: [
        "#FF7F11",
        "#FA9F42",
        "#F4C95D",
        "#FFD580",
        "#FFE4A1",
        "#FFF0C1",
        "#FFF7DC",
        "#FFFCF2",
      ],
      legend: {
        show: true,
        labels: {
          colors: [
            "#ffffff",
            "#ffffff",
            "#ffffff",
            "#ffffff",
            "#ffffff",
            "#ffffff",
            "#ffffff",
            "#ffffff",
          ],
        },
      },
      labels: genres,
      responsive: [
        {
          breakpoint: 480,
          options: {
            chart: { width: 200 },
            legend: { position: "bottom" },
          },
        },
      ],
    };

    const chart = new ApexCharts(
      el,
      chartConfig
    );
    chart.render();

    // Limpeza pra não ficar duplicando
    return () => {
      chart.destroy();
    };

    
  }, [infos]);

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
      console.log('Resposta da 2:', response.data);
      return response.data;
    } catch (error) {
      console.error('Erro ao gerar resposta da IA:', error);
      return 'Erro ao gerar mensagem da IA.';
    }
  }

  return (
    <div>
      <div className="bg-zinc-900 text-white p-6 rounded-2xl border-b-4 hover:shadow-zinc-950 mt-20 duration-300 border-amber-500 shadow-lg flex flex-col items-center gap-3 w-full max-w-2xl mx-auto">
      {/* Header */}
        <div className="relative mx-4 mt-4 flex flex-col items-center justify-center gap-4 overflow-hidden rounded-none bg-transparent bg-clip-border text-white shadow-none md:flex-row md:items-center">
          <div className="flex items-center justify-center">
            <h6 className="text-2xl font-bold  hover:text-amber-400 transition-colors">
              Gêneros em Destaque
            </h6>
          </div>
        </div>

      {/* Pie Chart and Message */}
      <div className="py-6 mt-4 grid place-items-center px-2">
        <div id="pie-chart"></div>
        <p className="mt-4 italic text-center text-gray-300 border-t border-gray-700 pt-4 px-4 duration-300">
          {AIMessage || "Carregando..."}
        </p>
      </div>
    </div>
  </div>
  );
};

export default GenreStats;
