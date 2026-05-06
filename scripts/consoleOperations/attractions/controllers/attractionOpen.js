import { APP_STRINGS } from '../../../strings.js';
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
      entityLabel: APP_STRINGS.entityLabels.attraction,
      optionsLabel: APP_STRINGS.entityLabels.attractions,
      payloadKey: 'attraction',
      resultName: result => result.attraction,
   });
}
