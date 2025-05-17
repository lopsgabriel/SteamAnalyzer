import { FC } from "react";

const LayoutFooter: FC = () => {
  return (
    <>
      <footer className="w-full text-center text-sm text-gray-400 py-6 border-t border-gray-800 bg-zinc-900">
        <p>
          Steam Analyzer © {new Date().getFullYear()} — Desenvolvido por Gabriel Lopes
        </p>
        <p className="mt-1">
          Dados obtidos via <a href="https://developer.valvesoftware.com/wiki/Steam_Web_API" target="_blank" className="underline hover:text-white">Steam Web API</a>. Este projeto não é afiliado à Valve Corporation.
        </p>
        <div className="flex justify-center gap-4 mt-4 text-gray-300">
          <a href="https://github.com/lopsgabriel" target="_blank" className="hover:text-white">GitHub</a>
          <a href="https://www.linkedin.com/in/lopsgabriel/" target="_blank" className="hover:text-white">LinkedIn</a>
        </div>
        <p className='mt-4'> Email: <a href="mailto:souzsgabriel12@gmail.com" className="underline hover:text-white">souzsgabriel12@gmail.com</a></p>
      </footer>
    </>
  );
};

export default LayoutFooter;
