import { useGeneralResultsData } from '@/hooks/useGeneralResultsData';
import { GeneralResultsChart } from '@/components/GeneralResultsChart';

export const GeneralResult = () => {
	const { data, isLoading, isError, results, extremes } = useGeneralResultsData();

	return (
		<div className="min-h-screen flex flex-col justify-center px-6 items-center">
			<div className="w-full max-w-6xl space-y-6">
				<div className="relative w-full h-[28rem] bg-white">
					{isLoading && (
						<div className="absolute inset-0 z-10 flex items-center justify-center bg-white bg-opacity-80">
							<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
						</div>
					)}

					{!isLoading && (isError || !data || data.length === 0) && (
						<div className="absolute inset-0 z-10 flex items-center justify-center bg-white bg-opacity-90">
							<p className="text-gray-600 text-lg">No hay datos disponibles para mostrar.</p>
						</div>
					)}

					<GeneralResultsChart results={results} />
				</div>
			</div>
		</div>
	);
};
