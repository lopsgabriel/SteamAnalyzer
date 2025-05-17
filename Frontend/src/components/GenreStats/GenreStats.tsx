import { FC, useEffect } from "react";
import { RiInformationLine } from "react-icons/ri";
import ApexCharts, { ApexOptions } from "apexcharts";
import MotionDiv from "../MotionDiv/MotionDiv";
interface GenreStatsProps {
  infos: {
    totalTimePlayed: number;
    totalTimePlayedPerGenre: Array<{ genre: string; time: number }>;
    totalGames: number;
    AImessage: string
    shorterTop5Games: Array<{ 
      name: string;
      hours: number;
       }>;
    };
}

const GenreStats: FC<GenreStatsProps> = ({ infos }) => {
  const AIMessage = infos.AImessage
  useEffect(() => {
    const genres = infos.totalTimePlayedPerGenre.map((g) => g.genre);
    const percentages = infos.totalTimePlayedPerGenre.map((g) =>
    g.time)

    const el = document.getElementById("pie-chart");
    if (!el) return;

    const chartConfig: ApexOptions = {
      series: percentages,
      chart: {
        type: "pie",
        width: 420,
        height: 420,
        toolbar: {
          show: false,
        },
      },
      title: {
        text: '',
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
          const value = opts.w.globals.series[opts.seriesIndex];
          return `${value.toLocaleString('pt-BR')} h`;
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

    return () => {
      chart.destroy();
    };

    
  }, [infos]);

  return (
    <div>
        <div className="bg-zinc-900 text-white p-6 rounded-2xl border-b-4 hover:shadow-zinc-900 mt-20 duration-300 border-amber-500 shadow-lg flex flex-col items-center gap-3 w-full max-w-2xl mx-auto">
          <MotionDiv>
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
              <p className="mt-4 italic text-center text-gray-300 border-t border-gray-700 hover:border-gray-500 pt-4 px-4 duration-300">
                {AIMessage}
              </p>

              <div className="w-full flex pt-4 px-4 items-start">
                <RiInformationLine className="w-4 h-4 text-gray-400 flex-none"/>
                <p className=" mx-2 italic text-gray-400 text-sm hover:text-gray-300 duration-300">
                  {`O gráfico mostra quais foram os generos mais jogados em horas. É possivel que um jogo tenha varios generos ao mesmo tempo.` }
                </p>
              </div>
            </div>
          </MotionDiv>
        </div>
      </div>
  );
};

export default GenreStats;
