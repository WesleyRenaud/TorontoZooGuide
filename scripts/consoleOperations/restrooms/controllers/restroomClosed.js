import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { populateRestroomDropdown } from '../../options/dropdowns.js';
import { loadRestrooms } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class RestroomClosed {
   static createRestroomClosedController({
      restroomEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: restroomEl,
         loadOptions: loadRestrooms,
         populateOptions: populateRestroomDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsApi.setRestroomClosed({
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
}
