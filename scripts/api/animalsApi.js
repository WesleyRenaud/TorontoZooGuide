import { ApiClient } from './apiClient.js';
import { AnimalViewingScope } from '../shared/enums/animalViewingScope.js';
import { ValueNormalizer } from './valueNormalizer.js';

function normalizeNamedList(items) {
   return ValueNormalizer.asArray(items)
      .map(ValueNormalizer.asTrimmedString)
      .filter(Boolean);
}

function normalizeRegion(region) {
   const source = ValueNormalizer.asObject(region);

   return {
      name: ValueNormalizer.asTrimmedString(source.name),
      hasExhibits: ValueNormalizer.asBoolean(source.hasExhibits),
   };
}

function normalizeAnimalInformation(animal) {
   const source = ValueNormalizer.asObject(animal);

   return {
      species: ValueNormalizer.asTrimmedString(source.species),
      latin_name: ValueNormalizer.asNullableString(source.latin_name),
      general_viewing_tips: ValueNormalizer.asNullableString(source.general_viewing_tips),
      seasonal_viewing_tips: ValueNormalizer.asNullableString(source.seasonal_viewing_tips),
      identification: ValueNormalizer.asNullableString(source.identification),
      habitat_and_range: ValueNormalizer.asNullableString(source.habitat_and_range),
      diet_and_feeding: ValueNormalizer.asNullableString(source.diet_and_feeding),
      behaviour_and_life_cycle: ValueNormalizer.asNullableString(source.behaviour_and_life_cycle),
      adaptations: ValueNormalizer.asNullableString(source.adaptations),
      reproduction_and_life_cycle: ValueNormalizer.asNullableString(source.reproduction_and_life_cycle),
      animals_at_the_zoo: ValueNormalizer.asNullableString(source.animals_at_the_zoo),
      exhibit: ValueNormalizer.asTrimmedString(source.exhibit),
      seasonal_viewing_summary: ValueNormalizer.asNullableString(source.seasonal_viewing_summary),
      seasonal_viewing_information: ValueNormalizer.asNullableString(source.seasonal_viewing_information),
   };
}

function normalizeRegionsResponse(response) {
   return normalizeNamedRegionList(ValueNormalizer.asObject(response).regions);
}

function normalizeNamedRegionList(regions) {
   return ValueNormalizer.asArray(regions)
      .map(normalizeRegion)
      .filter((region) => region.name);
}

function normalizeAnimalsResponse(response) {
   return normalizeNamedList(ValueNormalizer.asObject(response).animals);
}

function normalizeAnimalViewingScopesResponse(response) {
   const validScopes = new Set(Object.values(AnimalViewingScope));

   return normalizeNamedList(ValueNormalizer.asObject(response).viewingScopes)
      .filter(scope => validScopes.has(scope));
}

function normalizeExhibitsResponse(response) {
   return normalizeNamedList(ValueNormalizer.asObject(response).exhibits);
}

function normalizeAnimalInformationResponse(response) {
   const informationRows = ValueNormalizer.asArray(ValueNormalizer.asObject(response).information)
      .map(normalizeAnimalInformation)
      .filter((animal) => animal.species);

   return informationRows[0] ?? null;
}

export async function getRegions() {
   const response = await ApiClient.postJson('/get-regions', {});
   return normalizeRegionsResponse(response);
}

export async function getExhibitsInRegion(region) {
   const response = await ApiClient.postJson('/get-exhibits-in-region', { region });
   return normalizeExhibitsResponse(response);
}

export async function getAnimalsInExhibit(exhibit) {
   const response = await ApiClient.postJson('/get-animal-names-by-exhibit', { exhibit });
   return normalizeAnimalsResponse(response);
}

export async function getAnimalViewingScopes({ species, exhibit } = {}) {
   const response = await ApiClient.postJson('/get-animal-viewing-scopes', { species, exhibit });
   return normalizeAnimalViewingScopesResponse(response);
}

export async function getAnimalInformation({ species, exhibit }) {
   const response = await ApiClient.postJson('/get-animal-information', { species, exhibit });
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
