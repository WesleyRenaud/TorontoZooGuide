import { AnimalsApiNormalizer } from './animalsApiNormalizer.js';
import { ApiClient } from './apiClient.js';

export class AnimalsClient {
   static async getRegions() {
      const response = await ApiClient.postJson('/get-regions', {});
      return AnimalsApiNormalizer.normalizeRegionsResponse(response);
   }

   static async getExhibitsInRegion(region) {
      const response = await ApiClient.postJson('/get-exhibits-in-region', { region });
      return AnimalsApiNormalizer.normalizeExhibitsResponse(response);
   }

   static async getAnimalsInExhibit(exhibit) {
      const response = await ApiClient.postJson('/get-animal-names-by-exhibit', { exhibit });
      return AnimalsApiNormalizer.normalizeAnimalsResponse(response);
   }

   static async getAnimalViewingScopes({ species, exhibit } = {}) {
      const response = await ApiClient.postJson('/get-animal-viewing-scopes', { species, exhibit });
      return AnimalsApiNormalizer.normalizeAnimalViewingScopesResponse(response);
   }

   static async getAnimalInformation({ species, exhibit }) {
      const response = await ApiClient.postJson('/get-animal-information', { species, exhibit });
      return AnimalsApiNormalizer.normalizeAnimalInformationResponse(response);
   }
}
