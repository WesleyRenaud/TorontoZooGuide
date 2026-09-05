import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { populateGiftShopDropdown } from '../../options/dropdowns.js';
import { loadGiftShops } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export class GiftShopClosureOverride {
   static createGiftShopClosureOverrideController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: loadGiftShops,
         populateOptions: populateGiftShopDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsApi.setGiftShopClosureOverride({
               giftShop: entity,
               startDate: startDate || null,
               endDate: endDate || null,
               message,
            })
         ),
         entityLabel: APP_STRINGS.entityLabels.giftShop,
         optionsLabel: APP_STRINGS.entityLabels.giftShops,
         successMessage: result => APP_STRINGS.status.closureOverrideSaved(result.gift_shop),
      });
   }
}
