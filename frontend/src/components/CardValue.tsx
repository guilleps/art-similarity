import { Card } from './ui/card';
import { TrendingDown, TrendingUp } from 'lucide-react';

interface MetricCardProps {
	title: string;
	value: number;
	metric: string;
	type: 'max' | 'min';
	delay: number;
	/** Controls the overall compactness of the card */
	size?: 'sm' | 'md' | 'lg';
}

export const CardValue = ({ title, value, metric, type, delay, size = 'md' }: MetricCardProps) => {
	const Icon = type === 'max' ? TrendingUp : TrendingDown;
	const colorClass = type === 'max' ? 'text-green-400' : 'text-orange-400';
	const bgClass = type === 'max' ? 'bg-green-400/10' : 'bg-orange-400/10';

	const sizeClasses = {
		container: size === 'sm' ? 'p-3' : size === 'lg' ? 'p-7' : 'p-6',
		head: size === 'sm' ? 'mb-2' : size === 'lg' ? 'mb-5' : 'mb-4',
		iconWrap: size === 'sm' ? 'p-1.5' : size === 'lg' ? 'p-2.5' : 'p-2',
		icon: size === 'sm' ? 'h-4 w-4' : size === 'lg' ? 'h-6 w-6' : 'h-5 w-5',
		title: size === 'sm' ? 'text-[10px]' : size === 'lg' ? 'text-sm' : 'text-xs',
		gapY: size === 'sm' ? 'space-y-1' : size === 'lg' ? 'space-y-3' : 'space-y-2',
		value: size === 'sm' ? 'text-xl' : size === 'lg' ? 'text-3xl' : 'text-2xl',
		valueGap: size === 'sm' ? 'gap-1' : size === 'lg' ? 'gap-3' : 'gap-2',
		footer: size === 'sm' ? 'mt-2 pt-2' : size === 'lg' ? 'mt-5 pt-5' : 'mt-4 pt-4',
		badge: size === 'sm' ? 'w-1.5 h-1.5' : size === 'lg' ? 'w-2.5 h-2.5' : 'w-2 h-2',
		footerText: size === 'sm' ? 'text-[10px]' : size === 'lg' ? 'text-sm' : 'text-xs',
	};

	return (
		<>
			<Card
				className={`${sizeClasses.container} bg-gradient-card border-border/50 shadow-md hover:shadow-lg transition-all duration-300 animate-slide-up group hover:scale-105`}
				style={{ animationDelay: `${delay}ms` }}
			>
				<div className={`flex items-center justify-between ${sizeClasses.head}`}>
					<div className={`${sizeClasses.iconWrap} rounded-lg ${bgClass}`}>
						<Icon className={`${sizeClasses.icon} ${colorClass}`} />
					</div>
					<span
						className={`font-medium text-muted-foreground uppercase tracking-wider ${sizeClasses.title}`}
					>
						{title}
					</span>
				</div>

				<div className={`flex items-end justify-between ${sizeClasses.head}`}>
					<div className={`${sizeClasses.footer}`}>
						<div className="flex items-center gap-2">
							<div
								className={`${sizeClasses.badge} rounded-full ${type === 'max' ? 'bg-green-400' : 'bg-orange-400'}`}
							/>
							<span className={`${sizeClasses.footerText} text-muted-foreground`}>
								{type === 'max' ? 'Valor máximo detectado' : 'Valor mínimo detectado'}
							</span>
						</div>
					</div>

					<div className={`flex flex-col items-end ${sizeClasses.gapY}`}>
						<div className={`flex items-baseline justify-end ${sizeClasses.valueGap}`}>
							<span className={`${sizeClasses.value} font-bold text-foreground text-right`}>
								{value}
							</span>
						</div>
						<p className="text-sm text-muted-foreground text-right">Transformación: {metric}</p>
					</div>
				</div>
			</Card>
		</>
	);
};
