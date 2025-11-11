import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const getCarbonData = async () => {
	try {
		return axios.get(`${API_BASE}/carbon/`);
	} catch (error) {
		console.error('Error fetching carbon data:', error);
		throw error;
	}
};
