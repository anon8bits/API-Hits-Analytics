import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000';

export const fetchStats = async () => {
    const response = await axios.get(`${API_URL}/api/stats`);
    return response.data;
};

export const fetchRequestHistory = async (days) => {
    const response = await axios.get(`${API_URL}/api/requests`, {
        params: { days }
    });
    return response.data;
};

export const fetchColumnAggregate = async (column) => {
    const response = await axios.get(`${API_URL}/api/aggregate/${column}`);
    return response.data;
}   