import { setRestaurantOpeningSchedule } from '../../../api/consoleOperationsApi.js';
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
   });
}
