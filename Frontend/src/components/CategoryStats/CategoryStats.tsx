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
    <div className="section-container mt-20">
      <MotionDiv>
        <div className="bg-zinc-900 text-white rounded-2xl duration-300 flex flex-col items-center w-full max-w-2xl mx-auto">
          <h1 className="section-title">Categorias Mais Jogadas</h1>
          <ChartSection chartData={chartData} />
          <p className="section-message">
            {AIMessage}
          </p>
          <div className="w-full flex pt-4 px-4 ">
            <RiInformationLine className="w-4 h-4 text-gray-400 flex-none"/>
            <p className="info-text">
              {`O gráfico mostra as categorias mais jogadas em horas, um jogo é possivel conter diversas categorias ao mesmo tempo, inclusive Single-player e Multi-player simultaneamente.` }
            </p>
          </div>
        </div>
    </MotionDiv>
      </div>
  );
};

export default CategoryStats;