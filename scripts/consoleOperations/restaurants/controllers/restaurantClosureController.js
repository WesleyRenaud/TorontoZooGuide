import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityClosureControllerFactory } from '../../forms/amenityClosureControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RestaurantClosureController {
   static createRestaurantClosureOverrideController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return AmenityClosureControllerFactory.createAmenityClosureController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: ConsoleOptionsLoader.loadRestaurants,
         populateOptions: ConsoleDropdownPopulator.populateRestaurantDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsClient.setRestaurantClosureOverride({
               restaurant: entity,
               startDate: startDate || null,
               endDate: endDate || null,
               message,
            })
         ),
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: Strings.entityLabels.restaurants,
         resultName: result => result.restaurant,
      });
   }
}
