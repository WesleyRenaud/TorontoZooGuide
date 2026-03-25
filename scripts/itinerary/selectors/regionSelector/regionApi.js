import { postJson } from '../../../api/apiClient.js';
import { getItineraryDateSearchContext } from '../../itinerarySearchContext.js';

export async function getExhibitsByRegion() {
   const ctx = await getItineraryDateSearchContext();

   const result = await postJson('/get-exhibits-by-region', {
      month: ctx.month,
      day: ctx.day,
   });

   return Array.isArray(result?.regions) ? result.regions : [];
}

export async function getAnimalsByExhibit(exhibitsToInclude = []) {
   const ctx = await getItineraryDateSearchContext();

   const result = await postJson('/get-animals-by-exhibit', {
      month: ctx.month,
      day: ctx.day,
      temp: ctx.temp,
      exhibitsToInclude,
   });

   return Array.isArray(result?.animals) ? result.animals : [];
}