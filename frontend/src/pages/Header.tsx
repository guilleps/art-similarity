const Header = ({ currentPairIndex, paintingPairs }) => {
    return (
        <>
            <div className="text-center mb-12 animate-fade-in">
                <h2 className="text-3xl font-serif font-bold text-gallery-800 mb-4">
                    Resultados del Análisis de Transformaciones
                </h2>
                <p className="text-gallery-600">
                    Par {currentPairIndex} de {paintingPairs} • Evaluación de Similitud Composicional
                </p>
            </div>
        </>
    )
};

export default Header;