import { FC, useState } from "react";
import { motion } from "framer-motion";
import Card from "./ui/card";

interface FinalAnalysisProps {
  infos: {
    Username: string;
    Avatar: string;
    Tittle: string;
    Punchline: string;
    Description: string;
    Stats: Array<{ label: string; value: number }>;
    Img: string;
  };
}

const FinalAnalysis: FC<FinalAnalysisProps> = ({ infos }) => {
  console.log('FinalAnalysis infos →', infos);
  const [flipped, setFlipped] = useState(false);

  return (
    <div className="perspective-[1000px] w-full flex flex-col items-center  justify-center mt-32 mb-80">
      <h1 className="text-4xl font-bold text-center mb-10 font-onest hover:text-amber-500 hover:scale-105 duration-300"> Qual é o seu tipo de jogador?</h1>
      <motion.div
        className="relative w-[500px] h-[500px]"
        animate={{ rotateY: flipped ? 180 : 0 }}
        transition={{ duration: 0.8 }}
        style={{ transformStyle: 'preserve-3d' }}
        onClick={() => setFlipped(true)}
      >
        {/* FRENTE */}
        <div className="absolute w-full h-full backface-hidden bg-[#111] rounded-xl flex items-center justify-center text-white p-6">
          <h2 className="text-2xl font-bold text-center leading-tight">
            Clique para <br /> revelar <br /> seu estilo
          </h2>
        </div>

        {/* VERSO */}
        <div className="absolute w-full h-full backface-hidden rounded-xl text-white transform p-6" style={{ transform: 'rotateY(180deg)' }}>
          <Card infos={infos} />
        </div>
      </ motion.div>
    </div>
  );

};

export default FinalAnalysis;