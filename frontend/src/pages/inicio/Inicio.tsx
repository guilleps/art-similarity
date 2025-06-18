import { Navbar } from "../../components/Navbar";
import { BasicTerms } from "./BasicTerms";
import { HeroSection } from "./HeroSection";
import { ProblemSection } from "./ProblemSection";

export const Inicio = ({ basicTermOne, basicTermTwo, basicTermThree, selectedTerm }) => {
  return (
    <div className="space-y-0">
      <Navbar />

      <HeroSection />
      
      <ProblemSection />
      
      <BasicTerms
        selectedTerm={selectedTerm}
        onSelectTermOne={basicTermOne}
        onSelectTermTwo={basicTermTwo}
        onSelectTermThree={basicTermThree}
      />
    </div>
  );
};
