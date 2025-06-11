import { getAllSimilarities } from "@/services/similarity.service";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useEffect, useState } from "react";
import SimilarityViewer from "./par/SimilarityViewer";
import * as Dialog from "@radix-ui/react-dialog";

export const TableResults = () => {
    const [selectedRow, setSelectedRow] = useState<number | null>(null);
    const [currentPage, setCurrentPage] = useState<number>(0);
    const [transformations, setTransformations] = useState([])
    const [totalItems, setTotalItems] = useState<number>(0)
    const [selectedComparisonId, setSelectedComparisonId] = useState<string | null>(null);
    const [modalOpen, setModalOpen] = useState(false);

    const itemsPerPage = 10;
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    const handleRowClick = (comparison_id: string, rowPair: number) => {
        setSelectedRow(selectedRow === rowPair ? null : rowPair);
        // Scroll to comparison visualization
        if (selectedRow !== rowPair) {
            setTimeout(() => {
                const comparisonView = document.querySelector('.comparison-view');
                if (comparisonView) {
                    comparisonView.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, 100);
        }
        setSelectedComparisonId(comparison_id);
        setModalOpen(true);
    };

    useEffect(() => {
        const getSimilarities = async () => {
            try {
                const { data } = await getAllSimilarities(currentPage + 1, itemsPerPage);

                const transformedData = data.results.map((item, index) => ({
                    pair: index + 1 + currentPage * itemsPerPage,
                    tmcc: item.color_heat_map_transformation,
                    tt: item.tone_transformation,
                    ts: item.saturation_transformation,
                    tb: item.brightness_transformation,
                    tx: item.texture_transformation,
                    tc: item.contrast_transformation,
                    comparison_id: item.comparison_id
                }));

                setTransformations(transformedData);
                setTotalItems(data.count);
            } catch (err) {
                console.error("Error al cargar datos:", err);
            }
        };

        getSimilarities();
    }, [currentPage]);


    return (

        <div className="min-h-screen px-4 sm:px-6 lg:px-8 pt-12 pb-24 scroll-view">
            <div className="text-center space-y-6 max-w-6xl mx-auto">
                <div className="flex justify-center items-center space-x-4">
                    <h2 className="text-xl font-bold">Matriz de Resultados por Par similar</h2>
                </div>

                <div className="flex items-center justify-center space-x-4">
                    <button
                        onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
                        disabled={currentPage === 0}
                        className="p-2 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                    >
                        <ChevronLeft className="h-4 w-4" />
                    </button>

                    <span className="text-sm text-gray-600">
                        {currentPage * itemsPerPage + 1} - {Math.min((currentPage + 1) * itemsPerPage, totalItems)} › {totalItems}
                    </span>

                    <button
                        onClick={() => setCurrentPage(Math.min(totalPages - 1, currentPage + 1))}
                        disabled={currentPage === totalPages - 1}
                        className="p-2 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100"
                    >
                        <ChevronRight className="h-4 w-4" />
                    </button>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full border-collapse bg-white rounded-lg shadow mx-auto">
                        <thead>
                            <tr className="bg-gray-50">
                                <th className="border border-gray-200 px-4 py-2 text-left">N° Par</th>
                                <th className="border border-gray-200 px-4 py-2 text-left">TMCC</th>
                                <th className="border border-gray-200 px-4 py-2 text-left">TT</th>
                                <th className="border border-gray-200 px-4 py-2 text-left">TS</th>
                                <th className="border border-gray-200 px-4 py-2 text-left">TB</th>
                                <th className="border border-gray-200 px-4 py-2 text-left">TX</th>
                                <th className="border border-gray-200 px-4 py-2 text-left">TC</th>
                            </tr>
                        </thead>
                        <tbody>
                            {transformations.map((row) => (
                                <tr
                                    key={row.pair}
                                    className={`hover:bg-gray-50 cursor-pointer ${selectedRow === row.pair ? 'bg-blue-50' : ''
                                        }`}
                                    onClick={() => handleRowClick(row.comparison_id, row.pair)}
                                >
                                    <td className="border border-gray-200 px-4 py-2">{row.pair}</td>
                                    <td className="border border-gray-200 px-4 py-2">{row.tmcc}</td>
                                    <td className="border border-gray-200 px-4 py-2">{row.tt}</td>
                                    <td className="border border-gray-200 px-4 py-2">{row.ts}</td>
                                    <td className="border border-gray-200 px-4 py-2">{row.tb}</td>
                                    <td className="border border-gray-200 px-4 py-2">{row.tx}</td>
                                    <td className="border border-gray-200 px-4 py-2">{row.tc}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <Dialog.Root open={modalOpen} onOpenChange={setModalOpen}>
                <Dialog.Portal>
                    <Dialog.Overlay className="fixed inset-0 bg-black/50 z-40" />
                    <Dialog.Content
                        className="fixed z-50 top-1/2 left-1/2 max-w-5xl w-full h-[80vh] overflow-y-auto bg-white rounded-xl shadow-lg transform -translate-x-1/2 -translate-y-1/2"
                    >
                        {selectedComparisonId && <SimilarityViewer comparisonId={selectedComparisonId} />}
                    </Dialog.Content>
                </Dialog.Portal>
            </Dialog.Root>

        </div>
    )
};