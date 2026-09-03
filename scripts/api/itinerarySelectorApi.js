import { ApiClient } from './apiClient.js';
import { ValueNormalizer } from './valueNormalizer.js';

function normalizeRegion(region) {
   const source = ValueNormalizer.asObject(region);

   return {
      name: ValueNormalizer.asTrimmedString(source.name),
      exhibits: Array.isArray(source.exhibits)
         ? source.exhibits.map(ValueNormalizer.asTrimmedString).filter(Boolean)
         : [],
   };
}

function normalizeAnimal(animal) {
   const source = ValueNormalizer.asObject(animal);

   return {
      ...source,
      species: ValueNormalizer.asTrimmedString(source.species),
      exhibit: ValueNormalizer.asTrimmedString(source.exhibit),
   };
}

export async function getExhibitsByRegion(payload = {}) {
   const response = await ApiClient.postJson('/get-exhibits-by-region', payload);

   return Array.isArray(response?.regions)
      ? response.regions.map(normalizeRegion).filter((region) => region.name)
      : [];
}

export async function getAnimalsByExhibit(exhibitsToInclude, payload = {}) {
   const response = await ApiClient.postJson('/get-animals-by-exhibit', {
      ...payload,
      exhibitsToInclude,
   });

   return Array.isArray(response?.animals)
      ? response.animals.map(normalizeAnimal).filter((animal) => animal.species)
      : [];
}
