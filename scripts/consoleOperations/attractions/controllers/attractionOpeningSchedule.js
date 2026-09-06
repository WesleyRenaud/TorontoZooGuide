import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { OpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { WeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class AttractionOpeningSchedule {
   static createAttractionOpeningScheduleController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: Loaders.loadAttractions,
         populateOptions: Dropdowns.populateAttractionDropdown,
         submitSchedule: ConsoleOperationsApi.setAttractionOpeningSchedule,
         entityLabel: Strings.entityLabels.attraction,
         optionsLabel: Strings.entityLabels.attractions,
         payloadKey: 'attraction',
         resultName: result => result.attraction,
         resolveOverlapConflict: async payload => {
            const resolution = await OpeningScheduleOverlapDialog.showOpeningScheduleOverlapDialog();

            if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
               return ConsoleOperationsApi.replaceAttractionOpeningScheduleOverlaps(payload);
            }

            if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
               return ConsoleOperationsApi.trimAttractionOpeningScheduleOverlaps(payload);
            }

            return null;
         },
      });
   }
}
