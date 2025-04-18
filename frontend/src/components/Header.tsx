import LinkButton from './LinkButton'
import Logo from './Logo'

const Header = ({ completed }) => {
  return (
    <header className="flex items-center justify-between px-6 py-4">
      {completed ? (
        <>
          <Logo />

          <LinkButton
            to="/analysis"
            className="rounded-full bg-gradient-to-r from-purple-500 to-blue-500/55 px-5 py-2 text-sm font-medium text-white shadow-lg shadow-purple-500/20 transition-all duration-300 hover:translate-y-[-2px] hover:shadow-purple-500/30"
          >
            Pruébalo
          </LinkButton>
        </>
      ) : (
        <>
          <Logo />
        </>
      )}
    </header>
  )
}

export default Header
