"use client"
import { useState } from "react"
import { Bar, BarChart, LabelList, XAxis, YAxis, Cell } from "recharts"
import { Card, CardContent } from "./card"
import { type ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "./chart"

interface ChartSectionProps {
  chartData: Array<{ 
    name: string;
    hours: number;
     }>;
}

export function ChartSection( { chartData }: ChartSectionProps ) {  
  const [activeIndex, setActiveIndex] = useState<number | null>(null)

  const chartConfig = {
    hours: {
      label: "Desktop",
      color: "hsl(var(--chart-4))",
    },
  } satisfies ChartConfig


  return (
    <Card>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart
            accessibilityLayer
            data={chartData}
            layout="vertical"
            margin={{
              right: 16,
            }}
          >
            <YAxis
              dataKey="name"
              type="category"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              tickFormatter={(value) => value.slice(0, 3)}
              hide
            />
            <XAxis dataKey="hours" type="number" hide />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent indicator="line" />}
            />

            <Bar
              dataKey="hours"
              layout="vertical"
              radius={10}
              fill="white"
              onMouseEnter={(_, index) => setActiveIndex(index)}
              onMouseLeave={() => setActiveIndex(null)}
            >
              {
                chartData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={activeIndex === index ? "#f59e0b" : "#27272a"}
                    style={{
                      transition: "all 0.3s ease",
                      transform: activeIndex === index ? "scalex(1.02)" : "scalex(1)",
                      transformOrigin: "left center",
                    }}
                  />
                ))
              }
              <LabelList
                dataKey="name"
                position="insideLeft"
                offset={8}
                className="fill-white"
                fontSize={12}
                fontWeight="bold"
                fontFamily="Onest"
              />
              <LabelList
                dataKey="hours"
                position="right"
                className="fill-amber-400"
                fontSize={14}
                fontWeight={700}
                formatter={(value: number) => `${value} h`}
              />
            </Bar>
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}

export default ChartSection