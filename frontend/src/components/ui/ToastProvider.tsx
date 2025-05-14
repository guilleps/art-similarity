/* eslint-disable prettier/prettier */
import { Toaster } from 'sonner'
const ToastProvider = () => {
  return <Toaster 
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
}
export default ToastProvider;