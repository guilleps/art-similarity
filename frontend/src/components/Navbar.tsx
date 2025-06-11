import { useState, useEffect } from "react";
import { Link, NavLink } from "react-router-dom";
import { Menu, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

export const Navbar = () => {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            const isScrolled = window.scrollY > 20;
            if (isScrolled !== scrolled) {
                setScrolled(isScrolled);
            }
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, [scrolled]);

    const navigateItem = [
        { name: 'Inicio', path: '/' },
        { name: 'Contexto', path: '/contexto' },
        { name: 'Resultados', path: '/resultados' },
    ]

    return (
        <header className={cn("fixed top-0 left-0 right-0 z-50 transition-all duration-500", scrolled ? "bg-white/80 dark:bg-card/80 backdrop-blur-lg py-3 shadow-md" : "bg-transparent py-5")}>
            <nav className="container flex justify-center items-center">

                <ul className="hidden md:flex space-x-8">
                    {navigateItem.map(({ name, path }) => (
                        <li key={path} className="relative">
                            <NavLink
                                to={path}
                                className={({ isActive }) =>
                                    cn(
                                        "font-medium transition-colors after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:transition-all",
                                        isActive
                                            ? "text-blue-600 after:bg-blue-600 after:w-full"
                                            : "text-gray-600 hover:text-primary after:bg-blue-600 after:w-0 hover:after:w-full"
                                    )
                                }
                            >
                                {name}
                            </NavLink>
                        </li>
                    ))}
                </ul>

                <div className="md:hidden flex items-center space-x-2">
                    <Button variant="ghost" size="icon" onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="rounded-full">
                        {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                    </Button>
                </div>
            </nav>

            {/* Mobile Menu */}
            <div className={cn("fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden transition-opacity duration-500", mobileMenuOpen ? "opacity-100" : "opacity-0 pointer-events-none")}>
                <div className={cn("fixed inset-y-0 right-0 w-3/4 max-w-sm bg-card shadow-xl p-6 transition-transform duration-500 ease-in-out", mobileMenuOpen ? "translate-x-0" : "translate-x-full")}>
                    <div className="flex flex-col h-full justify-between">
                        <div>
                            <div className="flex justify-between mb-8">
                                <Button variant="ghost" size="icon" onClick={() => setMobileMenuOpen(false)} className="rounded-full">
                                    <X className="h-6 w-6" />
                                </Button>
                            </div>
                            <ul className="space-y-6">
                                {navigateItem.map(({ name, path }) => (
                                    <li key={path} className="relative">
                                        <NavLink to={path} className="text-lg font-medium transition-colors hover:text-primary" onClick={() => setMobileMenuOpen(false)}>
                                            {name}
                                        </NavLink>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
};
