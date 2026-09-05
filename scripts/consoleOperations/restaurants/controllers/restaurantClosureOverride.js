import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class RestaurantClosureOverride {
   static createRestaurantClosureOverrideController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: Loaders.loadRestaurants,
         populateOptions: Dropdowns.populateRestaurantDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsApi.setRestaurantClosureOverride({
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
}
