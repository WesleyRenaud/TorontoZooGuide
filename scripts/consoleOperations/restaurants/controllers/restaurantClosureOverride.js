import { setRestaurantClosureOverride } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { populateRestaurantDropdown } from '../../options/dropdowns.js';
import { loadRestaurants } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createRestaurantClosureOverrideController({
   restaurantEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: restaurantEl,
      loadOptions: loadRestaurants,
      populateOptions: populateRestaurantDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => (
         setRestaurantClosureOverride({
            restaurant: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         })
      ),
      entityLabel: APP_STRINGS.entityLabels.restaurant,
      optionsLabel: APP_STRINGS.entityLabels.restaurants,
      successMessage: result => APP_STRINGS.status.closureOverrideSaved(result.restaurant),
   });
}
