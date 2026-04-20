import { postJson } from './apiClient.js';
import {
   asObject,
   asTrimmedString,
} from './normalizeValues.js';

function normalizeRegion(region) {
   const source = asObject(region);

   return {
      name: asTrimmedString(source.name),
      exhibits: Array.isArray(source.exhibits)
         ? source.exhibits.map(asTrimmedString).filter(Boolean)
         : [],
   };
}

function normalizeAnimal(animal) {
   const source = asObject(animal);

   return {
      ...source,
      species: asTrimmedString(source.species),
      exhibit: asTrimmedString(source.exhibit),
   };
}

export async function getExhibitsByRegion(payload = {}) {
   const response = await postJson('/get-exhibits-by-region', payload);

   return Array.isArray(response?.regions)
      ? response.regions.map(normalizeRegion).filter((region) => region.name)
      : [];
}

export async function getAnimalsByExhibit(exhibitsToInclude, payload = {}) {
   const response = await postJson('/get-animals-by-exhibit', {
      ...payload,
      exhibitsToInclude,
   });

   return Array.isArray(response?.animals)
      ? response.animals.map(normalizeAnimal).filter((animal) => animal.species)
      : [];
}
