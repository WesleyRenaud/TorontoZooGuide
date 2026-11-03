import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpenControllerFactory } from '../../forms/amenityOpenControllerFactory.js';
import { EntityClosedControllerFactory } from '../../forms/entityClosedControllerFactory.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class GiftShopController {
   static createGiftShopClosedController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedControllerFactory.createEntityClosedController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: ConsoleOptionsLoader.loadGiftShops,
         populateOptions: ConsoleDropdownPopulator.populateGiftShopDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => ConsoleOperationsClient.setGiftShopClosed({
            giftShop: entity,
            startDate: startDate || null,
            endDate: endDate || null,
            message,
         }),
         entityLabel: Strings.entityLabels.giftShop,
         optionsLabel: Strings.entityLabels.giftShops,
         resultName: result => result.gift_shop,
      });
   }

   static createGiftShopClosedForSeasonController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: ConsoleOptionsLoader.loadGiftShops,
         populateOptions: ConsoleDropdownPopulator.populateGiftShopDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsClient.setGiftShopClosedForSeason({
               giftShop: entity,
               startDate: startDate || null,
               endDate: endDate || null,
               message,
            })
         ),
         entityLabel: Strings.entityLabels.giftShop,
         optionsLabel: Strings.entityLabels.giftShops,
         successMessage: result => Strings.status.closedForSeason(result.gift_shop),
      });
   }

   static createGiftShopOpenForSeasonController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpenControllerFactory.createAmenityOpenController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: ConsoleOptionsLoader.loadClosedForSeasonGiftShops,
         populateOptions: ConsoleDropdownPopulator.populateGiftShopDropdown,
         submitOpenStatus: ({ entity }) => ConsoleOperationsClient.setGiftShopOpenForSeason({
            giftShop: entity,
         }),
         entityLabel: Strings.entityLabels.giftShop,
         optionsLabel: Strings.entityLabels.giftShops,
         successMessage: result => Strings.status.openForSeason(result.gift_shop),
      });
   }
}
