import { APP_STRINGS } from '../../../strings.js';
import { loadRestaurants } from '../../options/loaders.js';
import { populateRestaurantDropdown } from '../../options/dropdowns.js';
import { createWeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { setRestaurantOpeningSchedule } from '../../../api/consoleOperationsApi.js';

export function createRestaurantOpenController({
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
