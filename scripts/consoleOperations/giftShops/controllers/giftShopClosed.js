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
      entityLabel: 'Gift shop',
      optionsLabel: 'gift shops',
      successMessage: result => `${result.gift_shop} was set as closed.`,
   });
}
