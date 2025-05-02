import { FC } from "react";
import ChartSection from "./ui/ChartSection";
import MotionDiv from "../MotionDiv/MotionDiv";

interface CategoryStatsProps {
  infos: {
    Username: string;
    ChartData: Array<{ name: string; hours: number }>;
  };
}


const CategoryStats: FC<CategoryStatsProps> = ({ infos }) => {

  const usuario = infos.Username
  const chartData = infos.ChartData

  return (
    <MotionDiv>
      <div>
        <div className="bg-zinc-900 text-white p-6 rounded-2xl border-b-4 hover:shadow-zinc-950 mt-20 duration-300 border-amber-500 shadow-lg flex flex-col items-center gap-3 w-full max-w-2xl mx-auto">
          <h1 className="text-2xl font-bold mb-4">Estatísticas de {usuario}</h1>
          <ChartSection chartData={chartData} />
        </div>
      </div>
    </MotionDiv>
  );
};

export default CategoryStats;