import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpenControllerFactory } from '../../forms/amenityOpenControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RestroomOpenController {
   static createRestroomOpenController({
      restroomEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpenControllerFactory.createAmenityOpenController({
         ...controllerOptions,
         entityEl: restroomEl,
         loadOptions: ConsoleOptionsLoader.loadRestrooms,
         populateOptions: ConsoleDropdownPopulator.populateRestroomDropdown,
         submitOpenStatus: ({ entity, startDate, endDate }) => ConsoleOperationsClient.setRestroomOpen({
            restroom: entity,
            startDate: startDate || null,
            endDate: endDate || null,
         }),
         entityLabel: Strings.entityLabels.restroom,
         optionsLabel: Strings.entityLabels.restrooms,
         resultName: result => result.restroom,
      });
   }
}
