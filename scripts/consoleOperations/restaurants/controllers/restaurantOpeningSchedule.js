import {
   replaceRestaurantOpeningScheduleOverlaps,
   setRestaurantOpeningSchedule,
   trimRestaurantOpeningScheduleOverlaps,
} from '../../../api/consoleOperationsApi.js';
import { OPENING_SCHEDULE_OVERLAP_RESOLUTION } from '../../forms/openingScheduleOverlap.js';
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
      submitSchedule: setRestaurantOpeningSchedule,
      entityLabel: APP_STRINGS.entityLabels.restaurant,
      optionsLabel: APP_STRINGS.entityLabels.restaurants,
      payloadKey: 'restaurant',
      resultName: result => result.restaurant,
      resolveOverlapConflict: async payload => {
         const resolution = await showOpeningScheduleOverlapDialog();

         if (resolution === OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
            return replaceRestaurantOpeningScheduleOverlaps(payload);
         }

         if (resolution === OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
            return trimRestaurantOpeningScheduleOverlaps(payload);
         }

         return null;
      },
   });
}
