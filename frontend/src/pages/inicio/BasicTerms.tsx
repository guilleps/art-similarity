const termContent = {
  caracteristicas: {
    title: "Características de bajo nivel",
    content: "Las características visuales de bajo nivel son atributos primarios de una imagen que no requieren interpretación cognitiva para ser detectados. Incluyen propiedades como color, textura, brillo, bordes y contraste. Estas características se extraen directamente a partir de los valores de píxeles mediante filtros o transformaciones simples. Son fundamentales en visión por computadora porque permiten describir visualmente una imagen antes de aplicar análisis más complejos o modelos de aprendizaje profundo."
  },
  transformaciones: {
    title: "Transformaciones visuales",
    content: "Las transformaciones visuales son operaciones aplicadas a una imagen para modificar aspectos específicos de su apariencia, como el color, la textura o la forma. Su propósito puede ser estético, funcional o experimental, y se utilizan comúnmente en aprendizaje automático para aumentar datos o probar la robustez de modelos. Sin embargo, una mala elección de transformaciones puede distorsionar características visuales esenciales, afectando negativamente el análisis, especialmente en contextos artísticos o estilísticos."
  },
  representaciones: {
    title: "Representaciones vectoriales",
    content: "Las representaciones vectoriales son formas numéricas en las que se codifican imágenes u objetos para facilitar su análisis computacional. Estas representaciones sintetizan múltiples características visuales en un solo vector multidimensional que puede ser comparado con otros mediante métricas matemáticas. Son esenciales en tareas como clasificación, búsqueda por similitud o recuperación de imágenes, ya que permiten analizar relaciones visuales sin necesidad de comparar directamente los píxeles originales de las imágenes."
  }
};

export const BasicTerms = ({
  selectedTerm,
  onSelectTermOne,
  onSelectTermTwo,
  onSelectTermThree,
}) => (
  <div className="min-h-screen flex flex-col items-center justify-center px-6 space-y-8 scroll-view">
    <div className="max-w-4xl mx-auto text-center space-y-6">
      <h2 className="text-2xl font-bold">Términos Básicos</h2>

      <div className="flex justify-center space-x-8">
        <button
          className={`pb-2 border-b-2 transition-all duration-500 ease-in-out ${selectedTerm === 'caracteristicas'
            ? 'text-blue-600 border-blue-600 font-medium'
            : 'text-gray-600 border-transparent hover:text-gray-800'
            }`}
          onClick={onSelectTermOne}
        >
          Características de bajo nivel
        </button>
        <button
          className={`pb-2 border-b-2 transition-all duration-500 ease-in-out ${selectedTerm === 'transformaciones'
            ? 'text-blue-600 border-blue-600 font-medium'
            : 'text-gray-600 border-transparent hover:text-gray-800'
            }`}
          onClick={onSelectTermTwo}
        >
          Transformaciones visuales
        </button>
        <button
          className={`pb-2 border-b-2 transition-all duration-500 ease-in-out ${selectedTerm === 'representaciones'
            ? 'text-blue-600 border-blue-600 font-medium'
            : 'text-gray-600 border-transparent hover:text-gray-800'
            }`}
          onClick={onSelectTermThree}
        >
          Representaciones vectoriales
        </button>
      </div>

      <div className="bg-gray-50 p-6 rounded-lg">
        <p className="text-gray-700 leading-relaxed text-justify">
          {termContent[selectedTerm].content}
        </p>
      </div>
    </div>
  </div>
);
