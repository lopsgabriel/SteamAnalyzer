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
    <div className="perspective-[1000px] w-full flex flex-col items-center pt-10  justify-center mt-20 mb-80">
      <motion.div
        className="relative w-[450px] h-[683px] cursor-pointer rounded-2xl"
        animate={{
          rotateY: flipped ? 180 : 0,
          boxShadow: flipped
            ? "0px 0px 0px rgba(255, 215, 0, 0)" // sem glow depois de virar
            : ["0px 0px 0px rgba(255, 215, 0, 0)", "0px 0px 20px rgba(255, 215, 0, 0.4)", "0px 0px 0px rgba(255, 215, 0, 0)"]
        }}
        transition={{
          duration: 2,
          repeat: flipped ? 0 : Infinity,
          ease: "easeInOut"
        }}
        style={{ transformStyle: 'preserve-3d' }}
        onClick={() => setFlipped(true)}
      >
        {/* VERSO */}
        <div className={`absolute w-full h-full backface-hidden rounded-xl text-white transform  `}>
            <CardBack />
        </div>

        {/* FRENTE */}
        <div className="absolute w-full h-full backface-hidden rounded-xl text-white transform " style={{ transform: 'rotateY(180deg)' }}>
          <Card infos={infos} />
        </div>
      </ motion.div>
    </div>
  );

};

export default FinalAnalysis;