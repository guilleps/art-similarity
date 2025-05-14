import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactNode } from 'react'
import { Toaster } from 'sonner'
import { ErrorBoundary } from './ErrorBoundary'

const queryClient = new QueryClient()

interface AppProvidersProps {
  children: ReactNode
}

const AppProviders = ({ children }: AppProvidersProps) => {
    return (
      <QueryClientProvider client={queryClient}>
        <ErrorBoundary>
          {children}
          <Toaster
            position="bottom-center"
            duration={4000}
            theme="dark"
            expand
            visibleToasts={3}
            toastOptions={{
              classNames: {
                title: 'text-white font-semibold text-base',
                description: 'text-white/60 text-sm',
                icon: 'hidden'
              }
            }}
          />
        </ErrorBoundary>
      </QueryClientProvider>
    )
  }
  
  export default AppProviders