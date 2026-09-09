import { EntityClosedFormController } from './entityClosedFormController.js';
import { Strings } from '../../strings.js';

export class AmenityClosureControllerFactory {
   static createAmenityClosureController({
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
         successMessage: result => Strings.status.closureOverrideSaved(resultName(result)),
      });
   }
}
