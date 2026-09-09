import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityClosureControllerFactory } from '../../forms/amenityClosureControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class GiftShopClosureController {
   static createGiftShopClosureOverrideController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return AmenityClosureControllerFactory.createAmenityClosureController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: ConsoleOptionsLoader.loadGiftShops,
         populateOptions: ConsoleDropdownPopulator.populateGiftShopDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsClient.setGiftShopClosureOverride({
               giftShop: entity,
               startDate: startDate || null,
               endDate: endDate || null,
               message,
            })
         ),
         entityLabel: Strings.entityLabels.giftShop,
         optionsLabel: Strings.entityLabels.giftShops,
         resultName: result => result.gift_shop,
      });
   }
}
