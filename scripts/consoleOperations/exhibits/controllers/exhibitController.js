import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityClosedControllerFactory } from '../../forms/entityClosedControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class ExhibitController {
   static createExhibitClosedController({
      exhibitEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedControllerFactory.createEntityClosedController({
         ...controllerOptions,
         entityEl: exhibitEl,
         loadOptions: ConsoleOptionsLoader.loadExhibits,
         populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsClient.setExhibitClosed({
            exhibit: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.exhibit,
         optionsLabel: Strings.entityLabels.exhibits,
         resultName: result => result.exhibit,
      });
   }
}
