import { FC } from "react";
import LayoutShell from "./ui/LayoutShell";
import Podium  from "./ui/Podium";
import GamesList from "./ui/GamesList";
import './ui/Styles.css'
import MotionDiv from "../MotionDiv/MotionDiv";


interface game {
  game:string,
  image: string
  appid: number
  progress_achievements: number
  hours: number
  total_achieved: number
}

interface TopGamesProps {
  info:{
    totalGames: number,
    AImessage: string,
    top5games: Array<game>
  }
}

export interface GameProps {
  id: string
  name: string
  avatar: string
  place: number
  hours: number
}


const TopGames: FC<TopGamesProps> = ({info}) => {
  const AIMessage = info.AImessage
  const podiumData = info.top5games.map((game, index) => ({
    id: game.appid.toString(),
    name: game.game,
    avatar: game.image,
    rank: index + 1,
    hours: game.hours 
  }))

  const Games = [...podiumData]
    .sort((a, b) => a.rank! - b.rank!)
    .map((GameProps, place) => ({ ...GameProps, place }))

  return(
    <LayoutShell AIMessage={AIMessage}>
        <MotionDiv>
          <Podium Games={Games} />
          <GamesList Games={Games} />
        </MotionDiv>
      </LayoutShell>
  )
}

export default TopGames