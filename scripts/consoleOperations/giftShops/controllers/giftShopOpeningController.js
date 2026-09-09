import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { AmenityOpeningScheduleControllerFactory } from '../../forms/amenityOpeningScheduleControllerFactory.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { ConsoleOptionsLoader } from '../../options/consoleOptionsLoader.js';
import { Strings } from '../../../strings.js';

export class GiftShopOpeningController {
   static createGiftShopOpeningScheduleController({
      giftShopEl,
      ...controllerOptions
   } = {}) {
      return AmenityOpeningScheduleControllerFactory.createAmenityOpeningScheduleController({
         ...controllerOptions,
         entityEl: giftShopEl,
         loadOptions: ConsoleOptionsLoader.loadGiftShops,
         populateOptions: ConsoleDropdownPopulator.populateGiftShopDropdown,
         submitSchedule: ConsoleOperationsClient.setGiftShopOpeningSchedule,
         entityLabel: Strings.entityLabels.giftShop,
         optionsLabel: Strings.entityLabels.giftShops,
         payloadKey: 'giftShop',
         resultName: result => result.gift_shop,
         replaceOverlaps: ConsoleOperationsClient.replaceGiftShopOpeningScheduleOverlaps,
         trimOverlaps: ConsoleOperationsClient.trimGiftShopOpeningScheduleOverlaps,
      });
   }
}
