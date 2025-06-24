import { GameProps } from '../TopGames'
import GameCard from './GamesCard'

interface Props {
  readonly Games: GameProps[]
}

export default function GamesList({ Games }: Props) {
  return (
    <div className="p-10">
      {Games.map((Game, index) => (
        <GameCard
          key={Game.id}
          Games={Games}
          Game={Game}
          index={index}
        />
      ))}
    </div>
  )
}
