import React from 'react'

interface Props {
  readonly children: React.ReactNode
}

export default function LayoutShell({ children }: Props) {
  return (
    <div className="App">
      <main className="container relative mx-auto bg-base-300 mt-20 rounded-xl border-b-2 border-amber-500 max-w-screen-sm pb-8">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:max-w-7xl lg:px-8">
          <h2 className="font-onest text-2xl text-center text-white w-full  p-3">
            Jogos Mais Jogados
          </h2>

          {children}
        </div>
      </main>
    </div>
  )
}
