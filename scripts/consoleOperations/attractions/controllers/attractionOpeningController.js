import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpeningScheduleControllerFactory } from '../../forms/amenityOpeningScheduleControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class AttractionOpeningController {
   static createAttractionOpeningScheduleController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpeningScheduleControllerFactory.createAmenityOpeningScheduleController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: ConsoleOptionsLoader.loadAttractions,
         populateOptions: ConsoleDropdownPopulator.populateAttractionDropdown,
         submitSchedule: ConsoleOperationsClient.setAttractionOpeningSchedule,
         entityLabel: Strings.entityLabels.attraction,
         optionsLabel: Strings.entityLabels.attractions,
         payloadKey: 'attraction',
         resultName: result => result.attraction,
         replaceOverlaps: ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps,
         trimOverlaps: ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps,
      });
   }
}
