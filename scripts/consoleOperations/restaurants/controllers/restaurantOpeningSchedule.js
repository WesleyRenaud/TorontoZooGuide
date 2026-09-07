import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { OpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { WeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RestaurantOpeningSchedule {
   static createRestaurantOpeningScheduleController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: ConsoleOptionsLoader.loadRestaurants,
         populateOptions: ConsoleDropdownPopulator.populateRestaurantDropdown,
         submitSchedule: ConsoleOperationsApi.setRestaurantOpeningSchedule,
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: Strings.entityLabels.restaurants,
         payloadKey: 'restaurant',
         resultName: result => result.restaurant,
         resolveOverlapConflict: async payload => {
            const resolution = await OpeningScheduleOverlapDialog.showOpeningScheduleOverlapDialog();

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
