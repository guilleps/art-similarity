export const Image = ({ image }) => {
    return (
        <>
            <div className="flex justify-center">
                <div className="relative group">
                    <img
                        src={image}
                        alt="Pintura izquierda"
                        className="w-50 h-50 object-cover rounded-lg shadow-lg transition-transform duration-300 group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-300 rounded-lg"></div>
                </div>
            </div>
        </>
    )
};