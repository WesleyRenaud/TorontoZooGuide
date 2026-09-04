import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { showOpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { createWeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { populateGiftShopDropdown } from '../../options/dropdowns.js';
import { loadGiftShops } from '../../options/loaders.js';
import { APP_STRINGS } from '../../../strings.js';

export function createGiftShopOpeningScheduleController({
   giftShopEl,
   ...controllerOptions
} = {}) {
   return createWeeklyAvailabilityFormController({
      ...controllerOptions,
      entityEl: giftShopEl,
      loadOptions: loadGiftShops,
      populateOptions: populateGiftShopDropdown,
      submitSchedule: ConsoleOperationsApi.setGiftShopOpeningSchedule,
      entityLabel: APP_STRINGS.entityLabels.giftShop,
      optionsLabel: APP_STRINGS.entityLabels.giftShops,
      payloadKey: 'giftShop',
      resultName: result => result.gift_shop,
      resolveOverlapConflict: async payload => {
         const resolution = await showOpeningScheduleOverlapDialog();

         if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
            return ConsoleOperationsApi.replaceGiftShopOpeningScheduleOverlaps(payload);
         }

         if (resolution === OpeningScheduleOverlap.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
            return ConsoleOperationsApi.trimGiftShopOpeningScheduleOverlaps(payload);
         }

         return null;
      },
   });
}
