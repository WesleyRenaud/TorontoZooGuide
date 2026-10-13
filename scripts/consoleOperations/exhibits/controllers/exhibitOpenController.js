import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpenControllerFactory } from '../../forms/amenityOpenControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class ExhibitOpenController {
   static createExhibitOpenController(refs) {
      return ExhibitOpenController.createController(refs, {
         loadOptions: ConsoleOptionsLoader.loadClosedExhibits,
         successMessage: result => Strings.status.explicitlyOpen(result.exhibit),
      });
   }

   static createExhibitOpenForSeasonController(refs) {
      return ExhibitOpenController.createController(refs, {
         loadOptions: ConsoleOptionsLoader.loadClosedForSeasonExhibits,
         successMessage: result => Strings.status.openForSeason(result.exhibit),
      });
   }

   static createController({
      exhibitEl,
      ...controllerOptions
   }, {
      loadOptions,
      successMessage,
   }) {
      return AmenityOpenControllerFactory.createAmenityOpenController({
         ...controllerOptions,
         entityEl: exhibitEl,
         loadOptions,
         populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
         submitOpenStatus: ({ entity, startDate, endDate }) => ConsoleOperationsClient.setExhibitOpen({
            exhibit: entity,
            startDate: startDate || null,
            endDate: endDate || null,
         }),
         entityLabel: Strings.entityLabels.exhibit,
         optionsLabel: Strings.entityLabels.exhibits,
         successMessage,
      });
   }
}
