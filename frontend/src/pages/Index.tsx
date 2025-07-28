import { Inicio } from './inicio/Inicio';
import { useAutoScrollView } from '@/hooks/useAutoScrollView';

export const Index = () => {
	// Auto-scroll functionality for views
	useAutoScrollView();

	return <Inicio />;
};
