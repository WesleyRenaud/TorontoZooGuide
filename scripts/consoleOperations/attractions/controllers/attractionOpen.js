import { loadAttractions } from '../../options/loaders.js';
import { populateAttractionDropdown } from '../../options/dropdowns.js';
import { createWeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { setAttractionOpeningSchedule } from '../../../api/consoleOperationsApi.js';

export function createAttractionOpenController({
   attractionEl,
   ...controllerOptions
} = {}) {
   return createWeeklyAvailabilityFormController({
      ...controllerOptions,
      entityEl: attractionEl,
      loadOptions: loadAttractions,
      populateOptions: populateAttractionDropdown,
      submitSchedule: setAttractionOpeningSchedule,
      entityLabel: 'Attraction',
      optionsLabel: 'attractions',
      payloadKey: 'attraction',
      resultName: result => result.attraction,
   });
}
