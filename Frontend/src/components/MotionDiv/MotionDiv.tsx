import React from "react";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";

interface MotionDivProps {
  children: React.ReactNode;
}

export default function MotionDiv({ children }: MotionDivProps) {

  const { ref: inViewRef, inView } = useInView({
    triggerOnce: true, // Só anima na primeira vez que entrar na tela
    threshold: 0.2     // Só considera "visível" quando 20% do bloco aparece
  });

  return (
    <motion.div
      ref={inViewRef} // Aqui é onde conectamos o observer
      className="w-full"
      initial={{ opacity: 0, y: 20 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
}