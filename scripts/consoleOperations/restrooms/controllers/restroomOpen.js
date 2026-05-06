import { APP_STRINGS } from '../../../strings.js';
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
      entityLabel: APP_STRINGS.entityLabels.restroom,
      optionsLabel: APP_STRINGS.entityLabels.restrooms,
      successMessage: result => APP_STRINGS.status.explicitlyOpen(result.restroom),
   });
}
