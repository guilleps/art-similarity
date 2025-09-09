import { Navbar } from '@/components/Navbar';
import { useAutoScrollView } from '@/hooks/useAutoScrollView';
import { HeroSection } from './inicio/HeroSection';
import { ProblemSection } from './inicio/ProblemSection';
import { BasicTerms } from './inicio/BasicTerms';

export const Index = () => {
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
