import { OpeningScheduleOverlapResolver } from './openingScheduleOverlapResolver.js';
import { WeeklyAvailabilityFormController } from './weeklyAvailabilityFormController.js';

export class AmenityOpeningScheduleControllerFactory {
   static createAmenityOpeningScheduleController({
      entityEl,
      loadOptions,
      populateOptions,
      submitSchedule,
      entityLabel,
      optionsLabel,
      payloadKey,
      resultName,
      replaceOverlaps,
      trimOverlaps,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl,
         loadOptions,
         populateOptions,
         submitSchedule,
         entityLabel,
         optionsLabel,
         payloadKey,
         resultName,
         resolveOverlapConflict: async payload => OpeningScheduleOverlapResolver.resolveOpeningScheduleOverlapConflict({
            payload,
            replaceOverlaps,
            trimOverlaps,
         }),
      });
   }
}
