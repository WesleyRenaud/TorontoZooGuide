import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpenControllerFactory } from '../../forms/amenityOpenControllerFactory.js';
import { EntityClosedControllerFactory } from '../../forms/entityClosedControllerFactory.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
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

   static createAttractionClosedForSeasonController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: ConsoleOptionsLoader.loadAttractions,
         populateOptions: ConsoleDropdownPopulator.populateAttractionDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsClient.setAttractionClosedForSeason({
               attraction: entity,
               startDate: startDate || null,
               endDate: endDate || null,
               message,
            })
         ),
         entityLabel: Strings.entityLabels.attraction,
         optionsLabel: Strings.entityLabels.attractions,
         successMessage: result => Strings.status.closedForSeason(result.attraction),
      });
   }

   static createAttractionOpenForSeasonController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpenControllerFactory.createAmenityOpenController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: ConsoleOptionsLoader.loadClosedForSeasonAttractions,
         populateOptions: ConsoleDropdownPopulator.populateAttractionDropdown,
         submitOpenStatus: ({ entity }) => ConsoleOperationsClient.setAttractionOpenForSeason({
            attraction: entity,
         }),
         entityLabel: Strings.entityLabels.attraction,
         optionsLabel: Strings.entityLabels.attractions,
         successMessage: result => Strings.status.openForSeason(result.attraction),
      });
   }
}
