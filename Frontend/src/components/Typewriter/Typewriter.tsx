import { FC, useEffect, useState } from "react";

const Typewriter: FC = () => {
  const words = ["Steam Analyzer", "Insira seu Perfil Steam",];
  const [text, setText] = useState("");
  const [index, setIndex] = useState(0); // qual palavra
  const [subIndex, setSubIndex] = useState(0); // posição da letra
  const [deleting, setDeleting] = useState(false);
  const [speed, setSpeed] = useState(100);

  useEffect(() => {
    if (index >= words.length) {
      setIndex(0);
      return;
    }

    const current = words[index];

    if (!deleting && subIndex === current.length) {
      setTimeout(() => setDeleting(true), 1200);
    } else if (deleting && subIndex === 0) {
      setDeleting(false);
      setIndex((prev) => (prev + 1) % words.length);
    }

    const timeout = setTimeout(() => {
      setText(current.substring(0, subIndex));
      setSubIndex(subIndex + (deleting ? -1 : 1));
    }, speed);

    return () => clearTimeout(timeout);
  }, [subIndex, index, deleting]);

  return (
    <div className="w-full flex justify-center items-center h-32">
      <h1 className="text-4xl font-bold font-sora">{text}<span className="animate-pulse">|</span></h1>
    </div>
  );
};

export default Typewriter;
