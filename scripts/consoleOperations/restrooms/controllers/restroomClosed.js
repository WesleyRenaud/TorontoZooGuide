import { setRestroomClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { populateRestroomDropdown } from '../../options/dropdowns.js';
import { loadRestrooms } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRestroomClosedController({
   restroomEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: restroomEl,
      loadOptions: loadRestrooms,
      populateOptions: populateRestroomDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => setRestroomClosed({
         restroom: entity,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
      }),
      entityLabel: APP_STRINGS.entityLabels.restroom,
      optionsLabel: APP_STRINGS.entityLabels.restrooms,
      successMessage: result => APP_STRINGS.status.closed(result.restroom),
   });
}
