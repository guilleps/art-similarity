interface SkeletonCardProps {
    className?: string;
}

export const SkeletonCard = ({ className = "w-[256px] h-[256px] bg-gray-300 animate-pulse rounded mx-auto shadow" }: SkeletonCardProps) => (
    <div
        className={`${className}`}
        style={{ aspectRatio: "1 / 1" }}
    />
);