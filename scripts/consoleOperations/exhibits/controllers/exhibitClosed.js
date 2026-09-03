import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { loadExhibits } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createExhibitClosedController({
   exhibitEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: exhibitEl,
      loadOptions: loadExhibits,
      populateOptions: populateExhibitDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsApi.setExhibitClosed({
         exhibit: entity,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
      }),
      entityLabel: APP_STRINGS.entityLabels.exhibit,
      optionsLabel: APP_STRINGS.entityLabels.exhibits,
      successMessage: result => APP_STRINGS.status.closed(result.exhibit),
   });
}
