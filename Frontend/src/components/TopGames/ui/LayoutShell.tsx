import React from 'react'

interface Props {
  readonly children: React.ReactNode
  readonly AIMessage: string
}

export default function LayoutShell({ children, AIMessage }: Props) {
  return (
    <div className="App">
      <main className="container relative bg-zinc-900 mt-20 rounded-xl border-b-4 border-amber-500 w-full max-w-2xl mx-auto pb-8 text-white py-6  hover:shadow-zinc-900 duration-300 shadow-lg gap-3">
        <div className="max-w-3xl mx-auto px-4 pt-10 sm:px-6 lg:max-w-7xl lg:px-8">
          <h2 className="font-onest text-center section-title">
            Jogos Mais Jogados
          </h2>
          {children}
        </div>
        <p className="section-message mx-8 whitespace-pre-wrap break-words max-h-48 overflow-y-auto">
        {AIMessage || "Carregando..."}
      </p>
      </main>
    </div>
  )
}
