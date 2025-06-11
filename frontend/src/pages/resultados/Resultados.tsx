import { Navbar } from "../../components/Navbar";
import { GeneralResult } from "./GeneralResult";
import SimilarityViewer from "./par/SimilarityViewer";
import { TableResults } from "./TableResults";
import { TransformResults } from "./TransformResults";

export const Resultados = () => {
    return (
        <div className="space-y-0">
            <Navbar />
            <GeneralResult />
            <TransformResults />
            <TableResults />
        </div>
    );
};