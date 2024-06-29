import api from './api';

export const getLocations = async () => {
  try {
    const response = await api.get('/locations');
    return response.data;
  } catch (error) {
    console.error('Error fetching locations:', error);
    throw error;
  }
};

export const getLocationsByPerson = async (personId) => {
  try {
    const response = await api.get(`/locations/person/${personId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching locations by person:', error);
    throw error;
  }
};

