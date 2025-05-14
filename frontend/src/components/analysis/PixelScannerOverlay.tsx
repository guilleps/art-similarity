import React from "react";

const PixelScannerOverlay = () => {
    const rows = 20
    const cols = 20
    const total = rows * cols

    return (
        <div className="absolute inset-0 z-10 grid grid-cols-20 grid-rows-20">
            {Array.from({ length: total }).map((_, i) => (
                <div
                    key={i}
                    className="bg-blue-400 mix-blend-lighten animate-[pixelBlink_1.5s_ease-in-out_infinite] opacity-10"
                    style={{
                        animationDelay: `${((i % cols) * 0.1 + Math.random() * 0.2).toFixed(2)}s`,
                        opacity: (Math.random() * 0.2 + 0.05).toFixed(2),
                    }}
                />
            ))}
        </div>
    )
}

export default PixelScannerOverlay