import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityOpenFormController } from '../../forms/entityOpenFormController.js';
import { populateRestroomDropdown } from '../../options/dropdowns.js';
import { loadRestrooms } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class RestroomOpen {
   static createRestroomOpenController({
      restroomEl,
      ...controllerOptions
   } = {}) {
      return EntityOpenFormController.createEntityOpenFormController({
         ...controllerOptions,
         entityEl: restroomEl,
         loadOptions: loadRestrooms,
         populateOptions: populateRestroomDropdown,
         submitOpenStatus: ({ entity, startDate, endDate }) => ConsoleOperationsApi.setRestroomOpen({
            restroom: entity,
            startDate: startDate || null,
            endDate: endDate || null,
         }),
         entityLabel: APP_STRINGS.entityLabels.restroom,
         optionsLabel: APP_STRINGS.entityLabels.restrooms,
         successMessage: result => APP_STRINGS.status.explicitlyOpen(result.restroom),
      });
   }
}
