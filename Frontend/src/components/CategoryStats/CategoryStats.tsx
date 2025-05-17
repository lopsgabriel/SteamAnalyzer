import { FC } from "react";
import ChartSection from "./ui/ChartSection";
import { RiInformationLine } from "react-icons/ri";
import MotionDiv from "../MotionDiv/MotionDiv";


interface CategoryStatsProps {
  infos: {
    ChartData: Array<{ name: string; hours: number }>;
    AImessage: string
  };
}


const CategoryStats: FC<CategoryStatsProps> = ({ infos }) => {
  const AIMessage = infos.AImessage
  const chartData = infos.ChartData

  return (
    <div className="bg-zinc-900 text-white p-6 rounded-2xl border-b-4 hover:shadow-zinc-900 mt-20 duration-300 border-amber-500 shadow-lg flex flex-col items-center gap-3 w-full max-w-2xl mx-auto">
      <MotionDiv>
        <div className="bg-zinc-900 text-white rounded-2xl duration-300 flex flex-col items-center w-full max-w-2xl mx-auto">
          <h1 className="text-2xl font-bold  hover:text-amber-400 transition-colors">Categorias Mais Jogadas</h1>
          <ChartSection chartData={chartData} />
          <p className="mt-4 italic text-center text-gray-300 border-t border-gray-700 hover:border-gray-500 pt-4 px-4 duration-300">
            {AIMessage}
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