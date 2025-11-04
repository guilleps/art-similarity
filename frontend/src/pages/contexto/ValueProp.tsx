export const ValueProp = ({
	icon,
	title,
	description,
}: {
	icon: React.ReactNode;
	title: string;
	description: string;
}) => {
	return (
		<div className="p-6 bg-gray-50 rounded-xl hover:shadow-lg transition-shadow">
			<div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4 mx-auto">
				{icon}
			</div>
			<h3 className="text-xl font-semibold mb-3 text-center">{title}</h3>
			<p className="text-gray-600 text-center">{description}</p>
		</div>
	);
};
