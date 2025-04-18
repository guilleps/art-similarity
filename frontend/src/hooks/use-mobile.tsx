import * as React from 'react'

const MOBILE_BREAKPOINT = 768 // tamaño base móvil

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean>(false)

  React.useEffect(() => {
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT) // setea estado inicial de la ventana

    const handleResize = () => {
      // responde ante el evento de ajuste de ventana
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    }

    window.addEventListener('resize', handleResize) // subscribe el evento de reajuste

    return () => window.removeEventListener('resize', handleResize) // descarta el evento para restaurarlo
  }, [])

  return isMobile
}
