import Logo from '../shared/Logo'

const Footer = () => {
  return (
    <footer className="border-t border-white/5 px-6 py-6">
      <div className="container mx-auto max-w-6xl">
        <div className="flex items-center justify-between">
          <Logo />
          <p className="text-sm text-white/40">
            © 2025 Vizel. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
