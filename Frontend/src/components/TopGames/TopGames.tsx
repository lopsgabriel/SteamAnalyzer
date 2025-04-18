import { FC, useEffect } from "react";
import LayoutShell from "./ui/LayoutShell";
import Podium  from "./ui/Podium";
import WinnersList from "./ui/WinnersList";
import './ui/Styles.css'


interface game {
  game:string,
  image: string
  appid: number
  progress_achievements: number
  time_played: number
  total_achieved: number
}

interface TopGamesProps {
  info:{
    Username: string,
    totalGames: number,
    top5games: Array<game>
  }
}

export interface Winner {
  id: string
  name: string
  avatar: string
  place: number
}


const TopGames: FC<TopGamesProps> = ({info}) => {
  const podiumData = info.top5games.map((game, index) => ({
    id: game.appid.toString(),
    name: game.game,
    avatar: game.image,
    rank: index + 1
  }))
  console.log(podiumData)
  console.log("info", info)
  console.log("top5games",info.top5games)

  useEffect(() => {
    console.log("podum", podiumData)
  },[])

  const winners = [...podiumData]
    .sort((a, b) => a.rank! - b.rank!)
    .map((winner, place) => ({ ...winner, place }))

  return(
    <LayoutShell>
      <Podium winners={winners} />
      <WinnersList winners={winners} />
    </LayoutShell>
  )
}

export default TopGames