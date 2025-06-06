import { Home } from "lucide-react";
import SimilarityViewer from './SimilarityViewer';
import { Link } from "react-router-dom";

const ResultsPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gallery-50 to-academic-50 p-8 relative">

      <Link
        to="/"
        className="bg-gallery-700 hover:bg-gallery-800 text-white px-6 py-3 rounded-full shadow-lg hover:scale-105"
      >
        <span className="hidden sm:inline">Volver al inicio</span>
      </Link>

      <SimilarityViewer />
    </div>
  );
};

export default ResultsPage;
