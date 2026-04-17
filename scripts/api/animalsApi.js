import { postJson } from './apiClient.js';

export async function getExhibitsInRegion(region) {
   const result = await postJson('/get-exhibits-in-region', { region });
   return result?.exhibits ?? [];
}

export async function getAnimalsInExhibit(exhibit) {
   const result = await postJson('/get-animal-names-by-exhibit', { exhibit });
   return result?.animals ?? [];
}

export async function getAnimalInformation(species) {
   const result = await postJson('/get-animal-information', { species });
   return (result?.information && result.information[0]) ? result.information[0] : null;
}

export function createAnimalsApi() {
   return {
      getExhibitsInRegion,
      getAnimalsInExhibit,
      getAnimalInformation
   };
}
