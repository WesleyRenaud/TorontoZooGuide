import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityClosedControllerFactory } from '../../forms/entityClosedControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class AttractionController {
   static createAttractionClosedController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedControllerFactory.createEntityClosedController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: ConsoleOptionsLoader.loadAttractions,
         populateOptions: ConsoleDropdownPopulator.populateAttractionDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsClient.setAttractionClosed({
            attraction: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.attraction,
         optionsLabel: Strings.entityLabels.attractions,
         resultName: result => result.attraction,
      });
   }
}
