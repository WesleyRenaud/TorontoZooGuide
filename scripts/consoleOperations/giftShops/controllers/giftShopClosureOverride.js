import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { EntityClosedFormController } from '../../forms/entityClosedFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class GiftShopClosureOverride {
   static createGiftShopClosureOverrideController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return EntityClosedFormController.createEntityClosedFormController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: Loaders.loadGiftShops,
         populateOptions: Dropdowns.populateGiftShopDropdown,
         submitClosedStatus: ({ entity, startDate, endDate, message }) => (
            ConsoleOperationsApi.setGiftShopClosureOverride({
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
