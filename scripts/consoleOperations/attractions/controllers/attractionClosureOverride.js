import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class AttractionClosureOverride {
   static createAttractionClosureOverrideController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: Loaders.loadAttractions,
         populateOptions: Dropdowns.populateAttractionDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsApi.setAttractionClosureOverride({
               attraction: entity,
               startDate: startDate || null,
               endDate: endDate || null,
               message,
            })
         ),
         entityLabel: APP_STRINGS.entityLabels.attraction,
         optionsLabel: APP_STRINGS.entityLabels.attractions,
         successMessage: result => APP_STRINGS.status.closureOverrideSaved(result.attraction),
      });
   }
}
