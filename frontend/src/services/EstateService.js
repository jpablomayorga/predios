import { apiClient } from './config.js';

const estatesPath = 'estates';

export default {
  getEstates(query='') {
    return apiClient.get(`${estatesPath}${query}`);
  },
  createEstate(
    name,
    cadastral_certificate,
    estate_registration,
    estate_type,
    owners) {
    console.log(arguments)
    return apiClient.post(estatesPath, {
      name,
      cadastral_certificate,
      estate_registration,
      estate_type,
      owners
    });
  },
  deleteEstate(uuid) {
    return apiClient.delete(`${estatesPath}/${uuid}`);
  },
  updateEstate(
    name,
    cadastral_certificate,
    estate_registration,
    estate_type,
    owners,
    uuid) {
    return apiClient.patch(`${estatesPath}/${uuid}`, {
      name,
      cadastral_certificate,
      estate_registration,
      estate_type,
      owners,
    });
  },
};
