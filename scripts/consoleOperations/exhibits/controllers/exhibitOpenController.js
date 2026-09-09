import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpenControllerFactory } from '../../forms/amenityOpenControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class ExhibitOpenController {
   static createExhibitOpenController({
      exhibitEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpenControllerFactory.createAmenityOpenController({
         ...controllerOptions,
         entityEl: exhibitEl,
         loadOptions: ConsoleOptionsLoader.loadExhibits,
         populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
         submitOpenStatus: ({ entity, startDate, endDate }) => ConsoleOperationsClient.setExhibitOpen({
            exhibit: entity,
            startDate: startDate || null,
            endDate: endDate || null,
         }),
         entityLabel: Strings.entityLabels.exhibit,
         optionsLabel: Strings.entityLabels.exhibits,
         resultName: result => result.exhibit,
      });
   }
}
