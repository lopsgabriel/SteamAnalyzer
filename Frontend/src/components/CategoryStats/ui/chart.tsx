"use client"

import {
  ResponsiveContainer,
  Tooltip as RechartsTooltip,
  TooltipProps,
} from "recharts"
import { cn } from "../../../lib"

export type ChartConfig = Record<
  string,
  { label: string; color: string }
>

export function ChartContainer({
  className,
  children,
}: {
  config: ChartConfig
  className?: string
  children: React.ReactElement
}) {
  // se quiser usar config no futuro, já tá aqui
  return (
    <ResponsiveContainer width="100%" height={340} className={cn(className)}>
      {children}
    </ResponsiveContainer>
  )
}

export function ChartTooltip(
  props: TooltipProps<number, string> & { cursor?: boolean }
) {
  return (
    <RechartsTooltip
      {...props}
      content={<ChartTooltipContent {...props} />} // aqui não tem `indicator`
    />
  )
}

export function ChartTooltipContent({
  active,
  payload,
  label, 
}: TooltipProps<number, string> & { indicator?: "line" | "bar" }) {
  if (!active || !payload?.length) return null

  const entry = payload[0]
  return (
    <div className="rounded-md border bg-popover px-3 py-2 text-sm shadow">
      <span className="font-medium">{label}</span>
      <div className="flex items-center gap-2">
        <span
          className="block h-2 w-2 rounded-full"
          style={{ background: entry.color }}
        />
        {entry.value}
      </div>
    </div>
  )
}
