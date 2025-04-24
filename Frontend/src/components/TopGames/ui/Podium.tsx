import { GameProps } from '../TopGames'
import PodiumStep from './PodiumStep'

interface Props {
  readonly Games: GameProps[]
}

export default function Podium({ Games }: Props) {
  const podium = [8, 6, 4, 2, 0, 1, 3, 5, 7, 9]
    .reduce(
      (podiumOrder, position) => [...podiumOrder, Games[position]],
      [] as readonly GameProps[]
    )
    .filter(Boolean)

  return (
    <div
      className="grid grid-flow-col-dense gap-2 mt-8 justify-center justify-items-center place-content-center content-end items-end border-b border-zinc-800"
      style={{ height: 250 }}
    >
      {podium.map((Game, index) => (
        <PodiumStep
          key={Game.id}
          podium={podium}
          Game={Game}
          index={index}
        />
      ))}
    </div>
  )
}
