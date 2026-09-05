import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class RestroomClosed {
   static createRestroomClosedController({
      restroomEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: restroomEl,
         loadOptions: Loaders.loadRestrooms,
         populateOptions: Dropdowns.populateRestroomDropdown,
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
