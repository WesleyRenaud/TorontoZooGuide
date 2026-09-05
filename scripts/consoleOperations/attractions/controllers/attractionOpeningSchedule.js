import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { WeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { populateAttractionDropdown } from '../../options/dropdowns.js';
import { loadAttractions } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class AttractionOpeningSchedule {
   static createAttractionOpeningScheduleController({
      attractionEl,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl: attractionEl,
         loadOptions: loadAttractions,
         populateOptions: populateAttractionDropdown,
         submitSchedule: ConsoleOperationsApi.setAttractionOpeningSchedule,
         entityLabel: APP_STRINGS.entityLabels.attraction,
         optionsLabel: APP_STRINGS.entityLabels.attractions,
         payloadKey: 'attraction',
         resultName: result => result.attraction,
         resolveOverlapConflict: async payload => {
            const resolution = await showOpeningScheduleOverlapDialog();

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
