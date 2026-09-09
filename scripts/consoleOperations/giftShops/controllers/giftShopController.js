import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityClosedControllerFactory } from '../../forms/entityClosedControllerFactory.js';
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
}
