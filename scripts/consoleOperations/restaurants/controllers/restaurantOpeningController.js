import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { OpeningScheduleChecker } from '../../forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapFragment } from '../../forms/openingScheduleOverlapFragment.js';
import { WeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RestaurantOpeningController {
   static createRestaurantOpeningScheduleController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: ConsoleOptionsLoader.loadRestaurants,
         populateOptions: ConsoleDropdownPopulator.populateRestaurantDropdown,
         submitSchedule: ConsoleOperationsClient.setRestaurantOpeningSchedule,
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: Strings.entityLabels.restaurants,
         payloadKey: 'restaurant',
         resultName: result => result.restaurant,
         resolveOverlapConflict: async payload => {
            const resolution = await OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();

            if (resolution === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
               return ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps(payload);
            }

            if (resolution === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
               return ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps(payload);
            }

            return null;
         },
      });
   }
}
