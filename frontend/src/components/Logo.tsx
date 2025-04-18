import { Link } from 'react-router-dom'

const Logo = () => {
  return (
    <Link to="/" className="flex items-center">
      <img src="/logo.png" alt="Vizel logo" className="h-10 w-auto" />
    </Link>
  )
}

export default Logo
