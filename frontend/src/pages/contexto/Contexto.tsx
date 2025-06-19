import { useAutoScrollView } from "@/hooks/useAutoScrollView";
import { Navbar } from "../../components/Navbar";
import { About } from "./About";
import { FlowSection } from "./FlowSection";

export const Contexto = () => {
    useAutoScrollView();
    
    return (
        <div className="space-y-0">
            <Navbar />

            <About />

            <FlowSection />
        </div >
    );
};