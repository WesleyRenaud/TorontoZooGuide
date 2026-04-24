import { loadRestaurants } from '../../options/loaders.js';
import { populateRestaurantDropdown } from '../../options/dropdowns.js';
import { setRestaurantClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';

export function createRestaurantClosedController({
   restaurantEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: restaurantEl,
      loadOptions: loadRestaurants,
      populateOptions: populateRestaurantDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => setRestaurantClosed({
         restaurant: entity,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
      }),
      entityLabel: 'Restaurant',
      optionsLabel: 'restaurants',
      successMessage: result => `${result.restaurant} was set as closed.`,
   });
}
