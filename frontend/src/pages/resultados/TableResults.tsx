import { getAllSimilarities, getExportedSimilarityData } from '@/services/similarity.service';
import { ChevronLeft, ChevronRight, FileDown, ChevronDown } from 'lucide-react';
import { useEffect, useState } from 'react';
import SimilarityViewer from './par/SimilarityViewer';
import * as Dialog from '@radix-ui/react-dialog';
import { Button } from '@/components/ui/button';

export const TableResults = () => {
	const [selectedRow, setSelectedRow] = useState<number | null>(null);
	const [currentPage, setCurrentPage] = useState<number>(0);
	const [transformations, setTransformations] = useState([]);
	const [totalItems, setTotalItems] = useState<number>(0);
	const [selectedComparisonId, setSelectedComparisonId] = useState<string | null>(null);
	const [modalOpen, setModalOpen] = useState(false);
	const [modalLoading, setModalLoading] = useState(true);
	const [showExportDropdown, setShowExportDropdown] = useState(false);

	const itemsPerPage = 10;
	const totalPages = Math.ceil(totalItems / itemsPerPage);

	const handleRowClick = (comparison_id: string, rowPair: number) => {
		setSelectedRow(rowPair);
		setSelectedComparisonId(comparison_id);
		setModalLoading(true); // reinicia loading
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
					comparison_id: item.comparison_id,
				}));

				setTransformations(transformedData);
				setTotalItems(data.count);
			} catch (err) {
				console.error('Error al cargar datos:', err);
			}
		};

		getSimilarities();
	}, [currentPage]);

	const exportData = async (format: 'json' | 'csv' = 'json') => {
		try {
			const response = await getExportedSimilarityData(format);
			let blob: Blob;

			if (format === 'csv') {
				// For CSV, the response is already a Blob
				blob = new Blob([response.data as unknown as BlobPart], {
					type: 'text/csv',
				});
			} else {
				// For JSON, we need to stringify the data
				blob = new Blob([JSON.stringify(response.data, null, 2)], {
					type: 'application/json',
				});
			}

			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = `similarity_results.${format}`;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);
		} catch (error) {
			console.error('Error al exportar datos:', error);
		}
	};

	return (
		<div className="min-h-screen px-4 sm:px-6 lg:px-8 pt-12 pb-12 scroll-view">
			<div className="text-center space-y-6 max-w-6xl mx-auto">
				<div className="flex justify-center items-center space-x-4">
					<h2 className="text-xl font-bold">Matriz de Resultados por Par similar</h2>
				</div>

				<div>
					<div className="flex items-center justify-between mt-6 pb-8">
						{/* Paginación */}
						<div className="flex items-center space-x-2">
							<Button
								onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
								disabled={currentPage === 0}
								variant="outline"
								className="inline-flex items-center px-3 py-1.5 text-sm font-medium"
							>
								<ChevronLeft className="h-4 w-4 mr-1" />
								Anterior
							</Button>

							<span className="text-sm text-gray-700">
								{currentPage * itemsPerPage + 1} -{' '}
								{Math.min((currentPage + 1) * itemsPerPage, totalItems)} de {totalItems}
							</span>

							<Button
								onClick={() => setCurrentPage(Math.min(totalPages - 1, currentPage + 1))}
								disabled={currentPage === totalPages - 1}
								variant="outline"
								className="inline-flex items-center px-3 py-1.5 text-sm font-medium"
							>
								Siguiente
								<ChevronRight className="h-4 w-4 ml-1" />
							</Button>
						</div>

						{/* Botón de exportación */}
						<div className="relative inline-block text-left">
							<button
								onClick={() => setShowExportDropdown(!showExportDropdown)}
								className="inline-flex items-center justify-between gap-2 px-4 py-2 text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded shadow"
							>
								<FileDown className="h-4 w-4" />
								Exportar
								<ChevronDown className="h-4 w-4 ml-1" />
							</button>

							{showExportDropdown && (
								<div className="absolute right-0 mt-2 w-40 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
									<div className="py-1">
										<button
											onClick={() => {
												setShowExportDropdown(false);
												exportData('json');
											}}
											className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
										>
											JSON
										</button>
										<button
											onClick={() => {
												setShowExportDropdown(false);
												exportData('csv');
											}}
											className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
										>
											CSV
										</button>
									</div>
								</div>
							)}
						</div>
					</div>

					<div className="overflow-x-auto">
						<table className="w-full border-collapse te bg-white rounded-lg shadow mx-auto">
							<thead>
								<tr className="hover:bg-gray-100 cursor-pointer">
									<th className="border border-gray-200 px-4 py-2 text-center">N° Par</th>
									<th className="border border-gray-200 px-4 py-2 text-center">TMCC</th>
									<th className="border border-gray-200 px-4 py-2 text-center">TT</th>
									<th className="border border-gray-200 px-4 py-2 text-center">TS</th>
									<th className="border border-gray-200 px-4 py-2 text-center">TB</th>
									<th className="border border-gray-200 px-4 py-2 text-center">TX</th>
									<th className="border border-gray-200 px-4 py-2 text-center">TC</th>
								</tr>
							</thead>
							<tbody>
								{transformations.map(row => (
									<tr
										key={row.pair}
										className={`hover:bg-gray-50 cursor-pointer ${
											selectedRow === row.pair ? 'bg-blue-50' : ''
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
			</div>

			<Dialog.Root open={modalOpen} onOpenChange={setModalOpen}>
				<Dialog.Portal>
					<Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40" />
					<Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 max-h-[90vh] w-full max-w-6xl overflow-auto rounded-lg bg-white p-6 shadow-lg z-50">
						<Dialog.Title className="sr-only">Detalles del par comparado</Dialog.Title>

						{modalLoading && (
							<div className="flex justify-center items-center min-h-[300px]">
								<div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
							</div>
						)}

						{selectedComparisonId && (
							<div className={modalLoading ? 'hidden' : ''}>
								<SimilarityViewer
									comparisonId={selectedComparisonId}
									onLoaded={() => setModalLoading(false)}
								/>
							</div>
						)}
					</Dialog.Content>
				</Dialog.Portal>
			</Dialog.Root>
		</div>
	);
};
