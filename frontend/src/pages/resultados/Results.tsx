import { Navbar } from '../../components/Navbar';
import { TableResults } from './TableResults';
import { TransformResults } from './TransformResults';
import { BoxPlotResults } from './BoxPlotResults';

export const Results = () => {
	return (
		<div className="space-y-0">
			<Navbar />
			<BoxPlotResults />
			<TransformResults />
			<TableResults />
		</div>
	);
};
