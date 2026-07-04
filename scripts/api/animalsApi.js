import { postJson } from './apiClient.js';
import {
   asArray,
   asBoolean,
   asNullableString,
   asObject,
   asTrimmedString,
} from './normalizeValues.js';
import { AnimalViewingScope } from '../shared/enums/animalViewingScope.js';

function normalizeNamedList(items) {
   return asArray(items)
      .map(asTrimmedString)
      .filter(Boolean);
}

function normalizeRegion(region) {
   const source = asObject(region);

   return {
      name: asTrimmedString(source.name),
      hasExhibits: asBoolean(source.hasExhibits),
   };
}

function normalizeAnimalInformation(animal) {
   const source = asObject(animal);

   return {
      species: asTrimmedString(source.species),
      latin_name: asNullableString(source.latin_name),
      general_viewing_tips: asNullableString(source.general_viewing_tips),
      seasonal_viewing_tips: asNullableString(source.seasonal_viewing_tips),
      identification: asNullableString(source.identification),
      habitat_and_range: asNullableString(source.habitat_and_range),
      diet_and_feeding: asNullableString(source.diet_and_feeding),
      behaviour_and_life_cycle: asNullableString(source.behaviour_and_life_cycle),
      adaptations: asNullableString(source.adaptations),
      reproduction_and_life_cycle: asNullableString(source.reproduction_and_life_cycle),
      animals_at_the_zoo: asNullableString(source.animals_at_the_zoo),
      exhibit: asTrimmedString(source.exhibit),
      seasonal_viewing_summary: asNullableString(source.seasonal_viewing_summary),
      seasonal_viewing_information: asNullableString(source.seasonal_viewing_information),
   };
}

function normalizeRegionsResponse(response) {
   return normalizeNamedRegionList(asObject(response).regions);
}

function normalizeNamedRegionList(regions) {
   return asArray(regions)
      .map(normalizeRegion)
      .filter((region) => region.name);
}

function normalizeAnimalsResponse(response) {
   return normalizeNamedList(asObject(response).animals);
}

function normalizeAnimalViewingScopesResponse(response) {
   const validScopes = new Set(Object.values(AnimalViewingScope));

   return normalizeNamedList(asObject(response).viewingScopes)
      .filter(scope => validScopes.has(scope));
}

function normalizeExhibitsResponse(response) {
   return normalizeNamedList(asObject(response).exhibits);
}

function normalizeAnimalInformationResponse(response) {
   const informationRows = asArray(asObject(response).information)
      .map(normalizeAnimalInformation)
      .filter((animal) => animal.species);

   return informationRows[0] ?? null;
}

export async function getRegions() {
   const response = await postJson('/get-regions', {});
   return normalizeRegionsResponse(response);
}

export async function getExhibitsInRegion(region) {
   const response = await postJson('/get-exhibits-in-region', { region });
   return normalizeExhibitsResponse(response);
}

export async function getAnimalsInExhibit(exhibit) {
   const response = await postJson('/get-animal-names-by-exhibit', { exhibit });
   return normalizeAnimalsResponse(response);
}

export async function getAnimalViewingScopes({ species, exhibit } = {}) {
   const response = await postJson('/get-animal-viewing-scopes', { species, exhibit });
   return normalizeAnimalViewingScopesResponse(response);
}

export async function getAnimalInformation({ species, exhibit }) {
   const response = await postJson('/get-animal-information', { species, exhibit });
   return normalizeAnimalInformationResponse(response);
}

export function createAnimalsApi() {
   return {
      getRegions,
      getExhibitsInRegion,
      getAnimalsInExhibit,
      getAnimalViewingScopes,
      getAnimalInformation,
   };
}
