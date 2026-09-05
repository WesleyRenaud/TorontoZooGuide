import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { WeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class RestaurantOpeningSchedule {
   static createRestaurantOpeningScheduleController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: Loaders.loadRestaurants,
         populateOptions: Dropdowns.populateRestaurantDropdown,
         submitSchedule: ConsoleOperationsApi.setRestaurantOpeningSchedule,
         entityLabel: APP_STRINGS.entityLabels.restaurant,
         optionsLabel: APP_STRINGS.entityLabels.restaurants,
         payloadKey: 'restaurant',
         resultName: result => result.restaurant,
         resolveOverlapConflict: async payload => {
            const resolution = await showOpeningScheduleOverlapDialog();

            if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
               return ConsoleOperationsApi.replaceRestaurantOpeningScheduleOverlaps(payload);
            }

            if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
               return ConsoleOperationsApi.trimRestaurantOpeningScheduleOverlaps(payload);
            }

            return null;
         },
      });
   }
}
