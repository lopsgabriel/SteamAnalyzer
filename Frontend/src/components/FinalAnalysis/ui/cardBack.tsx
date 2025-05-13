import { FC } from "react";
import teste2 from '../../../images/teste2.png';

const CardBack: FC = () => {
  
// const Card: FC = () => {
  return (
        <div className="flex flex-col items-center justify-center rounded-2xl border-y-4 border-amber-500">
          {/* Card wrapper – fixed MTG‑like aspect with rounded borders */}
          <div className="relative w-full aspect-[2/3] rounded-xl border-2 border-zinc-900 bg-zinc-900 ">
            <div className="border-b-2 border-zinc-800 flex flex-col items-center justify-center  rounded-lg m-4 mt-3 mb-3">
              <div className="relative flex items-center justify-center px-5 py-3 border-t-2 mt-5 border-zinc-600 w-full rounded-xl">
                <img src={teste2} alt="Steam" className="w-12 bg-zinc-900 h-12 absolute bottom-0.5 rounded-full " />
              </div>
              <h1 className='text-3xl font-bold text-center justify-center items-center flex mb-10 mt-44 font-onest hover:text-amber-500 hover:scale-105 duration-300'>
                  Qual é o seu tipo de jogador?
              </h1>
              <p className="text-lg text-center text-amber-500 justify-center items-center flex mb-10 font-onest hover:text-amber-500 hover:scale-105 duration-300">
                Clique e descubra!
              </p>
              {/* Bottom brand bar */}
              <div className=" relative top-2 flex items-center text-center pt-56 justify-center text-[10px] text-gray-400 uppercase">
                <p className=" flex justify-center px-4 bg-zinc-900">
                  Steam Analyzer
                </p>
              </div>
            </div>
          </div>
        </div>
  );
};

export default CardBack;