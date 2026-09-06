import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class AttractionClosed {
   static createAttractionClosedController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: Loaders.loadAttractions,
         populateOptions: Dropdowns.populateAttractionDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsApi.setAttractionClosed({
            attraction: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.attraction,
         optionsLabel: Strings.entityLabels.attractions,
         successMessage: result => Strings.status.closed(result.attraction),
      });
   }
}
