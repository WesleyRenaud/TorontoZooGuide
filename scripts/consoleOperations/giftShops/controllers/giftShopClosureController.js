import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class GiftShopClosureController {
   static createGiftShopClosureOverrideController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
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
         successMessage: result => Strings.status.closureOverrideSaved(result.gift_shop),
      });
   }
}
