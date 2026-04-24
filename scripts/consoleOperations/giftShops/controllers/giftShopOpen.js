import { loadGiftShops } from '../../options/loaders.js';
import { populateGiftShopDropdown } from '../../options/dropdowns.js';
import { createWeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { setGiftShopOpeningSchedule } from '../../../api/consoleOperationsApi.js';

export function createGiftShopOpenController({
   giftShopEl,
   ...controllerOptions
} = {}) {
   return createWeeklyAvailabilityFormController({
      ...controllerOptions,
      entityEl: giftShopEl,
      loadOptions: loadGiftShops,
      populateOptions: populateGiftShopDropdown,
      submitSchedule: setGiftShopOpeningSchedule,
      entityLabel: 'Gift shop',
      optionsLabel: 'gift shops',
      payloadKey: 'giftShop',
      resultName: result => result.gift_shop,
   });
}
