import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RestroomClosedController {
   static createRestroomClosedController({
      restroomEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: restroomEl,
         loadOptions: ConsoleOptionsLoader.loadRestrooms,
         populateOptions: ConsoleDropdownPopulator.populateRestroomDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsClient.setRestroomClosed({
            restroom: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.restroom,
         optionsLabel: Strings.entityLabels.restrooms,
         successMessage: result => Strings.status.closed(result.restroom),
      });
   }
}
