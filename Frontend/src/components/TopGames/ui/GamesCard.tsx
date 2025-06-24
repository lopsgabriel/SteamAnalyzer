import { motion } from 'framer-motion'
import { GameProps } from '../TopGames'
import { positions } from './constants'

interface Props {
  readonly Games: GameProps[]
  readonly Game: GameProps
  readonly index: number
}

export default function GameCard({ Games, Game, index }: Props) {
  const isWinner = Game.place === 0

  const maxHours = Math.max(...Games.map(game => game.hours || 0))

  // Calcula a porcentagem proporcional
  const progressWidth = maxHours > 0 
    ? Math.max(10, (Game.hours / maxHours) * 100) 
    : 10

  return (
    <motion.div
      custom={index}
      initial="hidden"
      animate="visible"
      variants={{
        visible: () => ({
          opacity: 1,
          y: 0,
          transition: {
            delay: 1 + (Games.length - Game.place + 1),
            duration: 0.75,
            ease: 'backInOut'
          }
        }),
        hidden: { opacity: 0, y: -100 }
      }}
      key={Game.id}
    >
      <div
        className={`flex items-center bg-zinc-800 my-3 rounded-xl shadow-md p-4 transition duration-300 ease-in-out transform hover:scale-105 hover:shadow-xl cursor-pointer group`}
      >
        <div className="text-lg font-bold w-10 text-amber-400">{positions[Game.place]}</div>

        <img
          src={Game.avatar}
          alt=""
          className={`rounded-full shadow-sm w-10 h-10 object-cover mr-4`}
        />

        <div className="flex-grow">
          <p className="text-gray-200 font-semibold group-hover:text-amber-500 duration-300 text-base leading-none">
            {Game.name || 'No name'}
          </p>
          <p className="text-gray-500 pt-1 text-sm">{typeof Game.hours === 'number' ? Game.hours.toLocaleString('pt-BR') : '0'} horas</p>

          <motion.div
            className="h-1 mt-2 bg-zinc-700 rounded-full overflow-hidden"
            initial={{ width: 0 }}
            animate={{ width: `${progressWidth}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          >
            <div
              className={`h-full transition-all duration-300 rounded-full ${
                isWinner ? 'bg-amber-400' : 'bg-amber-300'
              }`}
            />
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}
