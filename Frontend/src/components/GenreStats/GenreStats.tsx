import { FC, useEffect } from "react";
import ApexCharts from "apexcharts";

interface ChartData {
  genres: string[];
  percentages: number[];
}

interface GenreStatsProps {
  infos: {
    totalTimePlayed: number;
    totalTimePlayedPerGenre: Array<{ genre: string; time: number }>;
    totalGames: number;
  };
}

const GenreStats: FC<GenreStatsProps> = ({ infos }) => {


  useEffect(() => {
    const total = infos.totalTimePlayed;
    const genres = infos.totalTimePlayedPerGenre.map((g) => g.genre);
    const percentages = infos.totalTimePlayedPerGenre.map((g) =>
      total ? Math.round((g.time / total) * 100) : 0
    );

    const el = document.getElementById("pie-chart");
    if (!el) return;
    console.log("Elemento pie-chart existe?", el);

    const chartConfig = {
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
        show: false,
      },
      dataLabels: {
        enabled: true,
        style: {
          fontSize: "12px",
          colors: ["#ffffff"],
        },
      },
      colors: [
        "#443627", 
        "#D98324", 
        "#EFDCAB", 
        "#F2F6D0", 
        "#F57251",
        '#9CC4B2',
        '#B5A179',
        '#F3B79A',
      ]
      
      
      ,
      legend: { show: true },
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

  return (
    <div>
      <div className="relative flex flex-col rounded-xl bg-base-300 mt-20 bg-clip-border text-white shadow-md">
        <div className="relative mx-4 mt-4 flex flex-col gap-4 overflow-hidden rounded-none bg-transparent bg-clip-border text-white shadow-none md:flex-row md:items-center">
          <div className="w-max rounded-lg bg-gray-900 p-5 text-white">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="1.5"
              stroke="currentColor"
              aria-hidden="true"
              className="h-6 w-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3"
              ></path>
            </svg>
          </div>
          <div>
            <h6 className="text-base font-semibold text-blue-gray-900">
              Análise do Perfil
            </h6>
            <p className="max-w-sm text-sm text-white">
              Veja a distribuição de tempo e conquistas do perfil de Steam de
              forma visual e sarcástica!
            </p>
          </div>
        </div>
        <div className="py-6 mt-4 grid place-items-center px-2">
          <div id="pie-chart"></div>
        </div>
      </div>
    </div>
  );
};

export default GenreStats;
