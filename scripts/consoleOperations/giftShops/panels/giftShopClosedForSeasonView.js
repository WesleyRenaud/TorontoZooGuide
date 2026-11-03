import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class GiftShopClosedForSeasonView {
   static createGiftShopClosedForSeasonPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'giftShopClosedForSeasonPanel',
         title: Strings.panelTitles.giftShopClosedForSeason,
         entityLabel: Strings.entityLabels.giftShop,
         emptyOptionLabel: Strings.placeholders.giftShop,
         idPrefix: 'giftShopClosedForSeason',
         entityFieldName: 'GiftShop',
         startHelpText: Strings.help.startImmediately,
         endHelpText: Strings.help.keepClosedUntilManuallyReopened('gift shop'),
         messageLabel: Strings.labels.reason,
         messagePlaceholder: Strings.textareas.giftShopClosedForSeasonReason,
         submitId: 'submitGiftShopClosedForSeason',
         statusId: 'giftShopClosedForSeasonStatus',
      });
   }
}
