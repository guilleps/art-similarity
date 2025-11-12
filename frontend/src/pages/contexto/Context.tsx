import { Navbar } from '../../components/Navbar';
import { About } from './About';
import { FlowSection } from './FlowSection';

export const Context = () => {
	return (
		<div className="space-y-0">
			<Navbar />
			<About />
			<FlowSection />
		</div>
	);
};
