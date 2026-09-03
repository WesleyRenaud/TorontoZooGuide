import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { createEntityOpenFormController } from '../../forms/entityOpenFormController.js';
import { populateExhibitDropdown } from '../../options/dropdowns.js';
import { loadExhibits } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createExhibitOpenController({
   exhibitEl,
   ...controllerOptions
} = {}) {
   return createEntityOpenFormController({
      ...controllerOptions,
      entityEl: exhibitEl,
      loadOptions: loadExhibits,
      populateOptions: populateExhibitDropdown,
      submitOpenStatus: ({ entity, startDate, endDate }) => ConsoleOperationsApi.setExhibitOpen({
         exhibit: entity,
         startDate: startDate || null,
         endDate: endDate || null,
      }),
      entityLabel: APP_STRINGS.entityLabels.exhibit,
      optionsLabel: APP_STRINGS.entityLabels.exhibits,
      successMessage: result => APP_STRINGS.status.explicitlyOpen(result.exhibit),
   });
}
