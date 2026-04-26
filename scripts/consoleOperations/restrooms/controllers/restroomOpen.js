import { loadRestrooms } from '../../options/loaders.js';
import { populateRestroomDropdown } from '../../options/dropdowns.js';
import { setRestroomOpen } from '../../../api/consoleOperationsApi.js';
import { createEntityOpenFormController } from '../../forms/entityOpenFormController.js';

export function createRestroomOpenController({
   restroomEl,
   ...controllerOptions
} = {}) {
   return createEntityOpenFormController({
      ...controllerOptions,
      entityEl: restroomEl,
      loadOptions: loadRestrooms,
      populateOptions: populateRestroomDropdown,
      submitOpenStatus: ({ entity, startDate, endDate }) => setRestroomOpen({
         restroom: entity,
         startDate: startDate || null,
         endDate: endDate || null,
      }),
      entityLabel: 'Restroom',
      optionsLabel: 'restrooms',
      successMessage: result => `${result.restroom} was set as explicitly open.`,
   });
}
