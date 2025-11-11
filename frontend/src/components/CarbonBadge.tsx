import { getCarbonData } from '@/services/carbonService';
import { useEffect, useState } from 'react';

interface CarbonData {
	gco2e: number;
	cleanerThan: number;
}

export const CarbonBadge = () => {
	const [co2Data, setCo2Data] = useState<CarbonData | null>(null);

	useEffect(() => {
		const fetchData = async () => {
			const result = await getCarbonData();
			setCo2Data(result.data);
		};
		fetchData();
	}, []);

	if (!co2Data) return null;

	return (
		<div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-40 flex flex-col items-center gap-1">
			<div className="flex items-center gap-3 bg-white border border-border rounded-full px-4 py-2 shadow-sm">
				<span className="text-sm text-success font-medium">
					{co2Data.gco2e.toFixed(4)} g de CO₂/vista
				</span>
				<a
					href="https://www.websitecarbon.com/"
					target="_blank"
					rel="noopener noreferrer"
					className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium px-4 py-1.5 rounded-full transition-colors"
				>
					Website Carbon
				</a>
			</div>
			<p className="text-xs text-muted-foreground">
				Más limpio que el {co2Data.cleanerThan}% de las páginas probadas
			</p>
		</div>
	);
};
