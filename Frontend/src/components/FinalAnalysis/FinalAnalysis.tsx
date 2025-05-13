import { FC, useState } from "react";
import { motion } from "framer-motion";
import Card from "./ui/card";
import CardBack from "./ui/cardBack";

interface FinalAnalysisProps {
  infos: {
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
    <div className="perspective-[1000px] w-full flex flex-col items-center  justify-center mt-20 mb-80">
      <motion.div
        className="relative w-[500px] h-[500px]"
        animate={{ rotateY: flipped ? 180 : 0 }}
        transition={{ duration: 0.8 }}
        style={{ transformStyle: 'preserve-3d' }}
        onClick={() => setFlipped(!flipped)}
      >
        {/* VERSO */}
        <div className="absolute w-full h-full backface-hidden rounded-xl text-white transform p-6">
            <CardBack />
        </div>

        {/* FRENTE */}
        <div className="absolute w-full h-full backface-hidden rounded-xl text-white transform p-6" style={{ transform: 'rotateY(180deg)' }}>
          <Card infos={infos} />
        </div>
      </ motion.div>
    </div>
  );

};

export default FinalAnalysis;