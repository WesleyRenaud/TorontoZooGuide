import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityClosureControllerFactory } from '../../forms/amenityClosureControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class AttractionClosureController {
   static createAttractionClosureOverrideController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return AmenityClosureControllerFactory.createAmenityClosureController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: ConsoleOptionsLoader.loadAttractions,
         populateOptions: ConsoleDropdownPopulator.populateAttractionDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsClient.setAttractionClosureOverride({
               attraction: entity,
               startDate: startDate || null,
               endDate: endDate || null,
               message,
            })
         ),
         entityLabel: Strings.entityLabels.attraction,
         optionsLabel: Strings.entityLabels.attractions,
         resultName: result => result.attraction,
      });
   }
}
