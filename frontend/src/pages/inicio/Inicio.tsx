import { Navbar } from "../../components/Navbar";
import { BasicTerms } from "./BasicTerms";
import { HeroSection } from "./HeroSection";
import { ProblemSection } from "./ProblemSection";

export const Inicio = () => {
  return (
    <div className="space-y-0">
      <Navbar />

      <HeroSection />
      
      <ProblemSection />
      
      <BasicTerms />
    </div>
  );
};
