import { loadRestrooms } from '../../options/loaders.js';
import { populateRestroomDropdown } from '../../options/dropdowns.js';
import { setRestroomClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';

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
      entityLabel: 'Restroom',
      optionsLabel: 'restrooms',
      successMessage: result => `${result.restroom} was set as closed.`,
   });
}
