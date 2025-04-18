export const applyBodyGradient = () => {
  document.body.classList.add(
    'bg-gradient-radial',
    'from-[#10183d]',
    'to-[#080e24]'
  )
  document.body.style.background = '#080e24'
}

export const resetBodyGradient = () => {
  document.body.classList.remove(
    'bg-gradient-radial',
    'from-[#10183d]',
    'to-[#080e24]'
  )
  document.body.style.background = '#080e24'
}
