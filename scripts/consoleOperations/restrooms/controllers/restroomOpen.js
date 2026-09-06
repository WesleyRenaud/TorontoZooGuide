import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityOpenFormController } from '../../forms/entityOpenFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class RestroomOpen {
   static createRestroomOpenController({
      restroomEl,
      ...controllerOptions
   } = {}) {
      return EntityOpenFormController.createEntityOpenFormController({
         ...controllerOptions,
         entityEl: restroomEl,
         loadOptions: Loaders.loadRestrooms,
         populateOptions: Dropdowns.populateRestroomDropdown,
         submitOpenStatus: ({ entity, startDate, endDate }) => ConsoleOperationsApi.setRestroomOpen({
            restroom: entity,
            startDate: startDate || null,
            endDate: endDate || null,
         }),
         entityLabel: Strings.entityLabels.restroom,
         optionsLabel: Strings.entityLabels.restrooms,
         successMessage: result => Strings.status.explicitlyOpen(result.restroom),
      });
   }
}
