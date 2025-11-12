import { Toaster } from '@/components/ui/toaster';
import { Toaster as Sonner } from '@/components/ui/sonner';
import { TooltipProvider } from '@/components/ui/tooltip';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import NotFound from './pages/NotFound';
import { Context } from './pages/contexto/Context';
import { Results } from './pages/resultados/Results';
import { Index } from './pages/Index';
import { useState } from 'react';
import { FloatingButtons } from './components/FloatingButtonsProps';
import { SustainabilityModal } from './components/SustainabilityModal';
import { CarbonBadge } from './components/CarbonBadge';

const queryClient = new QueryClient();

const App = () => {
	const [isSostenibilityModalOpen, setIsSostenibilityModalOpen] = useState(false);

	return (
		<QueryClientProvider client={queryClient}>
			<TooltipProvider>
				<Toaster />
				<Sonner />
				<BrowserRouter>
					<Routes>
						<Route path="/" element={<Index />} />
						<Route path="/contexto" element={<Context />} />
						<Route path="/resultados" element={<Results />} />
						<Route path="*" element={<NotFound />} />
					</Routes>
				</BrowserRouter>
			</TooltipProvider>
			<CarbonBadge />
			<FloatingButtons onSustainabilityClick={() => setIsSostenibilityModalOpen(true)} />
			<SustainabilityModal
				open={isSostenibilityModalOpen}
				onOpenChange={setIsSostenibilityModalOpen}
			/>
		</QueryClientProvider>
	);
};

export default App;
