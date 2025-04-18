import { Winner } from '../TopGames'
import PodiumStep from './PodiumStep'

interface Props {
  readonly winners: Winner[]
}

export default function Podium({ winners }: Props) {
  const podium = [8, 6, 4, 2, 0, 1, 3, 5, 7, 9]
    .reduce(
      (podiumOrder, position) => [...podiumOrder, winners[position]],
      [] as readonly Winner[]
    )
    .filter(Boolean)

  return (
    <div
      className="grid grid-flow-col-dense gap-2 mt-8 justify-center justify-items-center place-content-center content-end items-end border-b "
      style={{ height: 250 }}
    >
      {podium.map((winner, index) => (
        <PodiumStep
          key={winner.id}
          podium={podium}
          winner={winner}
          index={index}
        />
      ))}
    </div>
  )
}
