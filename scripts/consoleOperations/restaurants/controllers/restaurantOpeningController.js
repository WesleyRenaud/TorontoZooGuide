import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpeningScheduleControllerFactory } from '../../forms/amenityOpeningScheduleControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class RestaurantOpeningController {
   static createRestaurantOpeningScheduleController({
      restaurantEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpeningScheduleControllerFactory.createAmenityOpeningScheduleController({
         ...controllerOptions,
         entityEl: restaurantEl,
         loadOptions: ConsoleOptionsLoader.loadRestaurants,
         populateOptions: ConsoleDropdownPopulator.populateRestaurantDropdown,
         submitSchedule: ConsoleOperationsClient.setRestaurantOpeningSchedule,
         entityLabel: Strings.entityLabels.restaurant,
         optionsLabel: Strings.entityLabels.restaurants,
         payloadKey: 'restaurant',
         resultName: result => result.restaurant,
         replaceOverlaps: ConsoleOperationsClient.replaceRestaurantOpeningScheduleOverlaps,
         trimOverlaps: ConsoleOperationsClient.trimRestaurantOpeningScheduleOverlaps,
      });
   }
}
