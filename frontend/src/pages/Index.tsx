import { Navbar } from '@/components/Navbar';
import { useAutoScrollView } from '@/hooks/useAutoScrollView';
import { HeroSection } from './inicio/HeroSection';
import { ProblemSection } from './inicio/ProblemSection';
import { BasicTerms } from './inicio/BasicTerms';
import { usePrefetchResultsData } from '@/hooks/usePrefetchResultsData';

export const Index = () => {
	usePrefetchResultsData();

	// Auto-scroll functionality for views
	useAutoScrollView();

	return (
		<div className="space-y-0">
			<Navbar />

			<HeroSection />

			<ProblemSection />

			<BasicTerms />
		</div>
	);
};
