import { Link } from 'react-router-dom'
import { cn } from '@/lib/utils'

type GradientLinkButtonProps = {
  to: string
  children: React.ReactNode
  className?: string
}

const LinkButton = ({ to, children, className }: GradientLinkButtonProps) => {
  return (
    <Link
      to={to}
      className={cn(
        `rounded-full font-medium text-white shadow-lg shadow-purple-500/20 transition-all duration-300 hover:translate-y-[-2px] hover:shadow-purple-500/30`,
        className
      )}
    >
      {children}
    </Link>
  )
}

export default LinkButton
