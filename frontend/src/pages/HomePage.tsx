import { Button } from '@/components/ui/button';
import { fetchSimilarityData } from '@/services/similarityService';
import { Play } from 'lucide-react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    const handleStart = async () => {
        setLoading(true);

        try {
            const data = await fetchSimilarityData();
            sessionStorage.setItem("initialSimilarityData", JSON.stringify(data));
            navigate("/results");
        } catch (e) {
            console.error("Error al iniciar", e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gallery-50 to-academic-100 flex items-center justify-center p-8">
            <div className="text-center max-w-4xl mx-auto animate-fade-in">
                <h1 className="text-5xl md:text-6xl font-serif font-bold text-gallery-800 mb-6 leading-tight">
                    Análisis de Similitud Composicional
                    <span className="text-academic-600 block">en Pinturas Impresionistas</span>
                </h1>
                <p className="text-xl md:text-2xl text-gallery-600 mb-12 leading-relaxed max-w-3xl mx-auto">
                    Resultados de la comparación de transformaciones aplicadas según características visuales de bajo nivel
                </p>
                <Button
                    onClick={handleStart}
                    size="lg"
                    className="bg-academic-600 hover:bg-academic-700 text-white px-8 py-4 text-lg font-medium rounded-full shadow-lg hover:scale-105"
                >
                    {loading ? (
                        <>
                            <span className="loader animate-spin mr-2 h-5 w-5 border-t-2 border-white border-solid rounded-full" />
                            Cargando...
                        </>
                    ) : (
                        <>
                            <Play className="mr-2 h-5 w-5" />
                            Comenzar
                        </>
                    )}
                </Button>
            </div>
        </div>
    );
};

export default HomePage;
