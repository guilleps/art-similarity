import { QueryClient } from '@tanstack/react-query'
import ToastProvider from './components/ui/ToastProvider'
import AppProviders from './app/providers'
import AppRouter from './app/router'

const queryClient = new QueryClient()

const App = () => (
  <AppProviders>
    <AppRouter />
  </AppProviders>
)

export default App
