import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpenControllerFactory } from '../../forms/amenityOpenControllerFactory.js';
import { EntityClosedControllerFactory } from '../../forms/entityClosedControllerFactory.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RestaurantController {
   static createRestaurantClosedController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedControllerFactory.createEntityClosedController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: ConsoleOptionsLoader.loadRestaurants,
         populateOptions: ConsoleDropdownPopulator.populateRestaurantDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsClient.setRestaurantClosed({
            restaurant: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: Strings.entityLabels.restaurants,
         resultName: result => result.restaurant,
      });
   }

   static createRestaurantClosedForSeasonController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: ConsoleOptionsLoader.loadRestaurants,
         populateOptions: ConsoleDropdownPopulator.populateRestaurantDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsClient.setRestaurantClosedForSeason({
               restaurant: entity,
               startDate: startDate || null,
               endDate: endDate || null,
               message,
            })
         ),
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: Strings.entityLabels.restaurants,
         successMessage: result => Strings.status.closedForSeason(result.restaurant),
      });
   }

   static createRestaurantOpenForSeasonController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpenControllerFactory.createAmenityOpenController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: ConsoleOptionsLoader.loadClosedForSeasonRestaurants,
         populateOptions: ConsoleDropdownPopulator.populateRestaurantDropdown,
         submitOpenStatus: ({ entity }) => ConsoleOperationsClient.setRestaurantOpenForSeason({
            restaurant: entity,
         }),
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: Strings.entityLabels.restaurants,
         successMessage: result => Strings.status.openForSeason(result.restaurant),
      });
   }
}
