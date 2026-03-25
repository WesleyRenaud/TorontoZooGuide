import { postJson } from '../../api/apiClient.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';

export async function searchSelectableAnimals({
   query = '',
   includeOffDisplayAnimals = false,
} = {}) {
   const ctx =
      typeof getItineraryDateSearchContext === 'function'
         ? await getItineraryDateSearchContext()
         : {};

   const payload = {
      query,
      includeAnimals: true,
      includeOffDisplayAnimals,
      ...ctx,
   };

   const response = await postJson('/search', payload);

   return (Array.isArray(response?.animals)
      ? response.animals
      : Array.isArray(response)
         ? response
         : response?.results) || [];
}