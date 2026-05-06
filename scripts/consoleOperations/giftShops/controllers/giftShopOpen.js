import { APP_STRINGS } from '../../../strings.js';
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
      entityLabel: APP_STRINGS.entityLabels.giftShop,
      optionsLabel: APP_STRINGS.entityLabels.giftShops,
      payloadKey: 'giftShop',
      resultName: result => result.gift_shop,
   });
}
