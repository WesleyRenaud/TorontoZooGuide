import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { OpeningScheduleOverlap } from '../../forms/openingScheduleOverlap.js';
import { OpeningScheduleOverlapDialog } from '../../forms/openingScheduleOverlapDialog.js';
import { WeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { Loaders } from '../../options/loaders.js';
import { Strings } from '../../../strings.js';

export class GiftShopOpeningSchedule {
   static createGiftShopOpeningScheduleController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: Loaders.loadGiftShops,
         populateOptions: Dropdowns.populateGiftShopDropdown,
         submitSchedule: ConsoleOperationsApi.setGiftShopOpeningSchedule,
         entityLabel: Strings.entityLabels.giftShop,
         optionsLabel: Strings.entityLabels.giftShops,
         payloadKey: 'giftShop',
         resultName: result => result.gift_shop,
         resolveOverlapConflict: async payload => {
            const resolution = await OpeningScheduleOverlapDialog.showOpeningScheduleOverlapDialog();

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
}
