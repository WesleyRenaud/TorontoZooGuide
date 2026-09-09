import { AmenityOpeningSchedulePanelBuilder } from '../../forms/amenityOpeningSchedulePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class GiftShopOpeningScheduleView {
   static createGiftShopOpeningSchedulePanel() {
      return AmenityOpeningSchedulePanelBuilder.createPanel({
         panelId: 'giftShopOpeningSchedulePanel',
         title: Strings.panelTitles.giftShopOpeningSchedule,
         entityLabel: Strings.entityLabels.giftShop,
         emptyOptionLabel: Strings.placeholders.giftShop,
         idPrefix: 'giftShopOpeningSchedule',
         entityFieldName: 'GiftShop',
         scheduleMessagePlaceholder: Strings.textareas.scheduledClosedMessage('gift shop'),
         submitId: 'submitGiftShopOpeningSchedule',
         statusId: 'giftShopOpeningScheduleStatus',
      });
   }
}
