import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { populateAttractionDropdown } from '../../options/dropdowns.js';
import { loadAttractions } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createAttractionClosedController({
   attractionEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: attractionEl,
      loadOptions: loadAttractions,
      populateOptions: populateAttractionDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsApi.setAttractionClosed({
         attraction: entity,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
      }),
      entityLabel: APP_STRINGS.entityLabels.attraction,
      optionsLabel: APP_STRINGS.entityLabels.attractions,
      successMessage: result => APP_STRINGS.status.closed(result.attraction),
   });
}
