import { APP_STRINGS } from '../../../strings.js';
import { loadGiftShops } from '../../options/loaders.js';
import { populateGiftShopDropdown } from '../../options/dropdowns.js';
import { setGiftShopClosed } from '../../../api/consoleOperationsApi.js';
import { createEntityClosedFormController } from '../../forms/entityClosedFormController.js';

export function createGiftShopClosedController({
   giftShopEl,
   ...controllerOptions
} = {}) {
   return createEntityClosedFormController({
      ...controllerOptions,
      entityEl: giftShopEl,
      loadOptions: loadGiftShops,
      populateOptions: populateGiftShopDropdown,
      submitClosedStatus: ({ entity, startDate, endDate, message }) => setGiftShopClosed({
         giftShop: entity,
         startDate: startDate || null,
         endDate: endDate || null,
         message,
      }),
      entityLabel: APP_STRINGS.entityLabels.giftShop,
      optionsLabel: APP_STRINGS.entityLabels.giftShops,
      successMessage: result => APP_STRINGS.status.closed(result.gift_shop),
   });
}
