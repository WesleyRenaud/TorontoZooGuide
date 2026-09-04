import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { createWeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { populateRestaurantDropdown } from '../../options/dropdowns.js';
import { loadRestaurants } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRestaurantOpeningScheduleController({
   restaurantEl,
   ...controllerOptions
} = {}) {
   return createWeeklyAvailabilityFormController({
      ...controllerOptions,
      entityEl: restaurantEl,
      loadOptions: loadRestaurants,
      populateOptions: populateRestaurantDropdown,
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
