import { AmenityClosedPanelBuilder } from '../../forms/amenityClosedPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class GiftShopClosedView {
   static createGiftShopClosedPanel() {
      return AmenityClosedPanelBuilder.createPanel({
         panelId: 'giftShopClosedPanel',
         title: Strings.panelTitles.giftShopClosed,
         entityLabel: Strings.entityLabels.giftShop,
         emptyOptionLabel: Strings.placeholders.giftShop,
         idPrefix: 'giftShopClosed',
         entityFieldName: 'GiftShop',
         endHelpText: Strings.help.continueUntilReopened('gift shop'),
         messageLabel: Strings.labels.closedMessage,
         messagePlaceholder: Strings.textareas.closedMessage('gift shop'),
         submitId: 'submitGiftShopClosed',
         statusId: 'giftShopClosedStatus',
      });
   }
}
