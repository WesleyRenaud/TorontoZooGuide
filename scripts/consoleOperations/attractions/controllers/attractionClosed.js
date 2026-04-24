import { loadAttractions } from '../../options/loaders.js';
import { populateAttractionDropdown } from '../../options/dropdowns.js';
import { setAttractionClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';

export function createAttractionClosedController({
   attractionEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: attractionEl,
      loadOptions: loadAttractions,
      populateOptions: populateAttractionDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => setAttractionClosed({
         attraction: entity,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
      }),
      entityLabel: 'Attraction',
      optionsLabel: 'attractions',
      successMessage: result => `${result.attraction} was set as closed.`,
   });
}
