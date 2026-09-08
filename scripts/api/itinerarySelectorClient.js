import { ApiClient } from './apiClient.js';
import { ItinerarySelectorApiNormalizer } from './itinerarySelectorApiNormalizer.js';

export class ItinerarySelectorClient {
   static async getExhibitsByRegion(payload = {}) {
      const response = await ApiClient.postJson('/get-exhibits-by-region', payload);

      return Array.isArray(response?.regions)
         ? response.regions.map(ItinerarySelectorApiNormalizer.normalizeRegion).filter((region) => region.name)
         : [];
   }

   static async getAnimalsByExhibit(exhibitsToInclude, payload = {}) {
      const response = await ApiClient.postJson('/get-animals-by-exhibit', {
         ...payload,
         exhibitsToInclude,
      });

      return Array.isArray(response?.animals)
         ? response.animals.map(ItinerarySelectorApiNormalizer.normalizeAnimal).filter((animal) => animal.species)
         : [];
   }
}
