import Footer from '@/components/Footer'
import Header from '@/components/Header'
import LinkButton from '@/components/LinkButton'

const Index = () => {
  return (
    <div className="flex h-screen flex-col overflow-hidden bg-[#080e24] bg-gradient-radial from-[#10183d] to-[#080e24]">
      <Header completed={true} />

      <section className="flex flex-1 flex-col items-center justify-center px-4 py-8 md:px-8 md:py-12">
        <div className="container mx-auto max-w-4xl text-center">
          <div className="mb-4 inline-block rounded-full border border-purple-500/30 bg-gradient-to-r from-purple-500/20 to-blue-500/20 px-6 py-2">
            <p className="bg-gradient-to-r to-white bg-clip-text text-sm">
              Explora las similitudes ocultas en la composición artística
            </p>
          </div>

          <h1 className="heading-gradient mb-4 text-3xl font-bold leading-tight tracking-tight sm:text-4xl md:mb-6 md:text-6xl lg:text-7xl">
            Descubra las similitudes en la esencia compositiva del arte
          </h1>

          <p className="mx-auto mb-8 max-w-2xl text-base text-white/60 md:text-lg">
            Deje que nuestro sofisticado algoritmo analice tu obra y detecte
            similitudes visuales en la composición.
          </p>

          <LinkButton
            to="/analysis"
            className="mx-auto flex w-fit items-center justify-center gap-2 rounded-full bg-gradient-to-r from-purple-500 to-blue-500/55 px-6 py-3 text-base font-medium text-white shadow-lg shadow-purple-500/20 transition-all duration-300 hover:translate-y-[-2px] hover:shadow-purple-500/30"
          >
            Cargar y analizar
          </LinkButton>
        </div>
      </section>

      <Footer />
    </div>
  )
}

export default Index
