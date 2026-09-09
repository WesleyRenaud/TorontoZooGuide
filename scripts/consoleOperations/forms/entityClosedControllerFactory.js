import { EntityClosedFormController } from './entityClosedFormController.js';
import { Strings } from '../../strings.js';

export class EntityClosedControllerFactory {
   static createEntityClosedController({
      entityEl,
      loadOptions,
      populateOptions,
      submitClosedStatus,
      entityLabel,
      optionsLabel,
      resultName,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl,
         loadOptions,
         populateOptions,
         submitClosedStatus,
         entityLabel,
         optionsLabel,
         successMessage: result => Strings.status.closed(resultName(result)),
      });
   }
}
