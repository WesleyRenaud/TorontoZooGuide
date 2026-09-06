import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class ExhibitClosed {
   static createExhibitClosedController({
      exhibitEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: exhibitEl,
         loadOptions: Loaders.loadExhibits,
         populateOptions: Dropdowns.populateExhibitDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsApi.setExhibitClosed({
            exhibit: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.exhibit,
         optionsLabel: Strings.entityLabels.exhibits,
         successMessage: result => Strings.status.closed(result.exhibit),
      });
   }
}
