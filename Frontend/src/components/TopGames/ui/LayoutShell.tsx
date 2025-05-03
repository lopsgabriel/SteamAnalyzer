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
          <h2 className="font-onest text-center text-2xl font-bold  hover:text-amber-400 transition-colors">
            Jogos Mais Jogados
          </h2>
          {children}
        </div>
        <p className="mt-4 mx-8 italic text-center text-gray-300 border-t border-gray-700 hover:border-gray-500 duration-300 pt-4 px-4 whitespace-pre-wrap break-words max-h-48 overflow-y-auto">
        {AIMessage || "Carregando..."}
      </p>
      </main>
    </div>
  )
}
