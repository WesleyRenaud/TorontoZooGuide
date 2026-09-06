import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class RestaurantClosed {
   static createRestaurantClosedController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: Loaders.loadRestaurants,
         populateOptions: Dropdowns.populateRestaurantDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsApi.setRestaurantClosed({
            restaurant: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: Strings.entityLabels.restaurants,
         successMessage: result => Strings.status.closed(result.restaurant),
      });
   }
}
