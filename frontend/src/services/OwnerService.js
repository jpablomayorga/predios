import { apiClient } from './config.js';

const ownersPath = 'owners';

export default {
  getOwners() {
    return apiClient.get(ownersPath);
  },
  createOwner(name, identification, owner_type) {
    return apiClient.post(ownersPath, {
      name,
      identification,
      owner_type
    });
  },
  deleteOwner(uuid) {
    return apiClient.delete(`${ownersPath}/${uuid}`);
  },
  updateOwner(name, identification, owner_type, uuid) {
    return apiClient.patch(`${ownersPath}/${uuid}`, {
      name,
      identification,
      owner_type
    });
  },
};
