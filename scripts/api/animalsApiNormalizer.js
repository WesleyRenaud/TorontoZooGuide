import { AnimalViewingModel } from '../shared/enums/animalViewingModel.js';
import { ValueNormalizer } from './valueNormalizer.js';

export class AnimalsApiNormalizer {
   static normalizeNamedList(items) {
      return ValueNormalizer.asArray(items)
         .map(ValueNormalizer.asTrimmedString)
         .filter(Boolean);
   }

   static normalizeRegion(region) {
      const source = ValueNormalizer.asObject(region);

      return {
         name: ValueNormalizer.asTrimmedString(source.name),
         hasExhibits: ValueNormalizer.asBoolean(source.hasExhibits),
      };
   }

   static normalizeAnimalInformation(animal) {
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

   static normalizeRegionsResponse(response) {
      return AnimalsApiNormalizer.normalizeNamedRegionList(ValueNormalizer.asObject(response).regions);
   }

   static normalizeNamedRegionList(regions) {
      return ValueNormalizer.asArray(regions)
         .map(AnimalsApiNormalizer.normalizeRegion)
         .filter((region) => region.name);
   }

   static normalizeAnimalsResponse(response) {
      return AnimalsApiNormalizer.normalizeNamedList(ValueNormalizer.asObject(response).animals);
   }

   static normalizeAnimalViewingScopesResponse(response) {
      const validScopes = new Set(Object.values(AnimalViewingModel));

      return AnimalsApiNormalizer.normalizeNamedList(ValueNormalizer.asObject(response).viewingScopes)
         .filter(scope => validScopes.has(scope));
   }

   static normalizeExhibitsResponse(response) {
      return AnimalsApiNormalizer.normalizeNamedList(ValueNormalizer.asObject(response).exhibits);
   }

   static normalizeAnimalInformationResponse(response) {
      const informationRows = ValueNormalizer.asArray(ValueNormalizer.asObject(response).information)
         .map(AnimalsApiNormalizer.normalizeAnimalInformation)
         .filter((animal) => animal.species);

      return informationRows[0] ?? null;
   }
}
