import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityOpenFormController } from '../../forms/entityOpenFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class ExhibitOpen {
   static createExhibitOpenController({
      exhibitEl,
      ...controllerOptions
   } = {}) {
      return EntityOpenFormController.createEntityOpenFormController({
         ...controllerOptions,
         entityEl: exhibitEl,
         loadOptions: Loaders.loadExhibits,
         populateOptions: Dropdowns.populateExhibitDropdown,
         submitOpenStatus: ({ entity, startDate, endDate }) => ConsoleOperationsApi.setExhibitOpen({
            exhibit: entity,
            startDate: startDate || null,
            endDate: endDate || null,
         }),
         entityLabel: Strings.entityLabels.exhibit,
         optionsLabel: Strings.entityLabels.exhibits,
         successMessage: result => Strings.status.explicitlyOpen(result.exhibit),
      });
   }
}
