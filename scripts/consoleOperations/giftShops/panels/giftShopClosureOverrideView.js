import { AmenityClosureOverridePanelBuilder } from '../../forms/amenityClosureOverridePanelBuilder.js';
import { Strings } from '../../../strings.js';

export class GiftShopClosureOverrideView {
   static createGiftShopClosureOverridePanel() {
      return AmenityClosureOverridePanelBuilder.createPanel({
         panelId: 'giftShopClosureOverridePanel',
         title: Strings.panelTitles.giftShopClosureOverride,
         entityLabel: Strings.entityLabels.giftShop,
         emptyOptionLabel: Strings.placeholders.giftShop,
         idPrefix: 'giftShopClosureOverride',
         entityFieldName: 'GiftShop',
         endHelpText: Strings.help.continueUntilReopened('gift shop'),
         messageLabel: Strings.labels.closedMessage,
         messagePlaceholder: Strings.textareas.closedMessage('gift shop'),
         submitId: 'submitGiftShopClosureOverride',
         statusId: 'giftShopClosureOverrideStatus',
      });
   }
}
