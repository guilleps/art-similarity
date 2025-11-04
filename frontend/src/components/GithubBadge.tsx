import { Github } from 'lucide-react';

export const GithubBadge = () => {
	return (
		<a
			href="https://github.com/guilleps/art-similarity"
			target="_blank"
			rel="noopener noreferrer"
			className="fixed bottom-6 right-6 bg-gray-900 hover:bg-gray-800 text-white rounded-full p-3 shadow-lg transition-all duration-300"
			title="Ver en GitHub"
		>
			<Github className="w-6 h-6" />
		</a>
	);
};
