import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class ExhibitController {
   static createExhibitClosedController(refs) {
      return ExhibitController.createController(refs, {
         isClosedForSeason: false,
         successMessage: result => Strings.status.closed(result.exhibit),
      });
   }

   static createExhibitClosedForSeasonController(refs) {
      return ExhibitController.createController(refs, {
         isClosedForSeason: true,
         successMessage: result => Strings.status.closedForSeason(result.exhibit),
      });
   }

   static createController({
      exhibitEl,
      ...controllerOptions
   }, {
      isClosedForSeason,
      successMessage,
   }) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: exhibitEl,
         loadOptions: ConsoleOptionsLoader.loadExhibits,
         populateOptions: ConsoleDropdownPopulator.populateExhibitDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsClient.setExhibitClosed({
            exhibit: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
            isClosedForSeason,
         }),
         entityLabel: Strings.entityLabels.exhibit,
         optionsLabel: Strings.entityLabels.exhibits,
         successMessage,
      });
   }
}
