export const ValueProp = ({
    icon,
    title,
    description
}: {
    icon: React.ReactNode,
    title: string,
    description: string
}) => {
    return (
        <div className="flex flex-col items-center text-center p-6">
            <div className="w-16 h-16 flex items-center justify-center rounded-full bg-blue-100 mb-4">
                {icon}
            </div>
            <h3 className="text-xl font-bold mb-3">{title}</h3>
            <p className="text-foreground/80">{description}</p>
        </div>
    );
};