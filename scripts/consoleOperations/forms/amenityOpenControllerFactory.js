import { EntityOpenFormController } from './entityOpenFormController.js';
import { Strings } from '../../strings.js';

export class AmenityOpenControllerFactory {
   static createAmenityOpenController({
      entityEl,
      loadOptions,
      populateOptions,
      submitOpenStatus,
      entityLabel,
      optionsLabel,
      resultName,
      successMessage,
      ...controllerOptions
   } = {}) {
      return EntityOpenFormController.createEntityOpenFormController({
         ...controllerOptions,
         entityEl,
         loadOptions,
         populateOptions,
         submitOpenStatus,
         entityLabel,
         optionsLabel,
         successMessage: successMessage ?? (result => Strings.status.explicitlyOpen(resultName(result))),
      });
   }
}
