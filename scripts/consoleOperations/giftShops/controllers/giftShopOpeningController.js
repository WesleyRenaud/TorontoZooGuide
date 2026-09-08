import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { OpeningScheduleChecker } from '../../forms/openingScheduleChecker.js';
import { OpeningScheduleOverlapFragment } from '../../forms/openingScheduleOverlapFragment.js';
import { WeeklyAvailabilityFormController } from '../../forms/weeklyAvailabilityFormController.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class GiftShopOpeningController {
   static createGiftShopOpeningScheduleController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return WeeklyAvailabilityFormController.createWeeklyAvailabilityFormController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: ConsoleOptionsLoader.loadGiftShops,
         populateOptions: ConsoleDropdownPopulator.populateGiftShopDropdown,
         submitSchedule: ConsoleOperationsClient.setGiftShopOpeningSchedule,
         entityLabel: Strings.entityLabels.giftShop,
         optionsLabel: Strings.entityLabels.giftShops,
         payloadKey: 'giftShop',
         resultName: result => result.gift_shop,
         resolveOverlapConflict: async payload => {
            const resolution = await OpeningScheduleOverlapFragment.showOpeningScheduleOverlapDialog();

            if (resolution === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.REPLACE) {
               return ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps(payload);
            }

            if (resolution === OpeningScheduleChecker.OPENING_SCHEDULE_OVERLAP_RESOLUTION.TRIM) {
               return ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps(payload);
            }

            return null;
         },
      });
   }
}
