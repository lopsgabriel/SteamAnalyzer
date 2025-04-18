import { motion } from 'framer-motion'
import { Winner } from '../TopGames'
import { positions } from './constants'

interface Props {
  readonly podium: Winner[]
  readonly winner: Winner
  readonly index: number
}

export default function PodiumStep({ podium, winner, index }: Props) {
  return (
    <div className="flex flex-col place-content-center">
      <motion.div
        custom={index}
        initial="hidden"
        animate="visible"
        variants={{
          visible: () => ({
            opacity: 1,
            transition: {
              delay: 1 + (podium.length - winner.place + 2),
              duration: 0.50
            }
          }),
          hidden: { opacity: 0 }
        }}
        className="mb-1 self-center"
      >
        <img
          src={winner.avatar}
          alt=""
          className="rounded-full border border-black shadow-sm w-13 h-13 hover:scale-110 hover:shadow-md duration-300 ease-in-out" 
        />
      </motion.div>
      <motion.div
        custom={index}
        initial="hidden"
        animate="visible"
        variants={{
          visible: () => ({
            height: 200 * ((podium.length - winner.place) / podium.length),
            opacity: 2,
            transition: {
              delay: 1 + (podium.length - winner.place),
              duration: 1.5,
              ease: 'backInOut'
            }
          }),
          hidden: { opacity: 0, height: 0 }
        }}
        className="bg-amber-500 flex w-16 border-black border border-b-0 rounded-t-lg shadow-lg place-content-center hover:border-amber-900 hover:bg-amber-400 cursor-pointer"
        style={{
          marginBottom: -1,
          filter: `opacity(${
            0.1 + (podium.length - winner.place) / podium.length
          })`
        }}
      >
        <span className="self-end text-white font-semibold">
          {positions[winner.place]}
        </span>
      </motion.div>
    </div>
  )
}
