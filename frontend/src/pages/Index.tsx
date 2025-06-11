import { useEffect, useState } from "react";
import { Inicio } from "./inicio/Inicio";

export const Index = () => {
  const [currentInterface, setCurrentInterface] = useState<'inicio' | 'contexto' | 'resultados'>('inicio');

  // Move all useState hooks to the top level
  const [selectedTerm, setSelectedTerm] = useState<'caracteristicas' | 'transformaciones' | 'representaciones'>('caracteristicas');


  const interfaceNames = {
    inicio: 'Inicio',
    contexto: 'Contexto',
    resultados: 'Resultados'
  };

  // Auto-scroll functionality for views
  useEffect(() => {
    const handleScroll = () => {
      const views = document.querySelectorAll('.scroll-view');
      const scrollY = window.scrollY;
      const windowHeight = window.innerHeight;

      views.forEach((view, index) => {
        const rect = view.getBoundingClientRect();
        const viewTop = rect.top + scrollY;
        const viewBottom = viewTop + rect.height;

        // Check if view is mostly in viewport
        if (scrollY + windowHeight / 2 >= viewTop && scrollY + windowHeight / 2 <= viewBottom) {
          // Smooth scroll to center the view
          if (Math.abs(rect.top) > 10) {
            view.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }
      });
    };

    const throttledScroll = () => {
      clearTimeout(window.scrollTimeout);
      window.scrollTimeout = setTimeout(handleScroll, 100);
    };

    window.addEventListener('scroll', throttledScroll);
    return () => window.removeEventListener('scroll', throttledScroll);
  }, []);

  return (
    <Inicio
      viewsResultButton={() => setCurrentInterface('resultados')}
      basicTermOne={() => setSelectedTerm('caracteristicas')}
      basicTermTwo={() => setSelectedTerm('transformaciones')}
      basicTermThree={() => setSelectedTerm('representaciones')}
      selectedTerm={selectedTerm}
    />
  );
};