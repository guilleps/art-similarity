import { Leaf } from 'lucide-react';

export const SostenibilityBadge = () => {
	return (
		<a
			href="https://github.io/artshift/sustainability"
			target="_blank"
			rel="noopener noreferrer"
			className="fixed bottom-24 right-6 bg-[#57e389] hover:bg-green-500 text-black rounded-full p-3 shadow-lg transition-all duration-300"
			title="CO2"
		>
			<Leaf className="w-6 h-6" />
		</a>
	);
};
