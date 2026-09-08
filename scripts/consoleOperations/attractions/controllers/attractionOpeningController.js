import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { OpeningScheduleChecker } from '../../forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapFragment } from '../../forms/openingScheduleOverlapFragment.js';
import { WeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class AttractionOpeningController {
   static createAttractionOpeningScheduleController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: ConsoleOptionsLoader.loadAttractions,
         populateOptions: ConsoleDropdownPopulator.populateAttractionDropdown,
         submitSchedule: ConsoleOperationsClient.setAttractionOpeningSchedule,
         entityLabel: Strings.entityLabels.attraction,
         optionsLabel: Strings.entityLabels.attractions,
         payloadKey: 'attraction',
         resultName: result => result.attraction,
         resolveOverlapConflict: async payload => {
            const resolution = await OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();

            if (resolution === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
               return ConsoleOperationsClient.replaceAttractionOpeningScheduleOverlaps(payload);
            }

            if (resolution === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
               return ConsoleOperationsClient.trimAttractionOpeningScheduleOverlaps(payload);
            }

            return null;
         },
      });
   }
}
