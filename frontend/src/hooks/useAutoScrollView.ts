import { useEffect } from "react";

export const useAutoScrollView = () => {
    useEffect(() => {
        let scrollTimeout: NodeJS.Timeout;

        const handleScroll = () => {
            const views = document.querySelectorAll('.scroll-view');
            const scrollY = window.scrollY;
            const windowHeight = window.innerHeight;

            views.forEach((view) => {
                const rect = view.getBoundingClientRect();
                const viewTop = rect.top + scrollY;
                const viewBottom = viewTop + rect.height;

                // Check if view is mostly in viewport
                if (scrollY + windowHeight / 2 >= viewTop && scrollY + windowHeight / 2 <= viewBottom) {
                    // Smooth scroll to center the view
                    if (Math.abs(rect.top) > 10) {
                        view.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        }

        const throttledScroll = () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(handleScroll, 100);
        }

        window.addEventListener("scroll", throttledScroll);
        return () => window.removeEventListener("scroll", throttledScroll);
    }, []);
};