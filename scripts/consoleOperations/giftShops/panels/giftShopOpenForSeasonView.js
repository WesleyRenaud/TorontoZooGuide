import { AmenityOpenPanelBuilder } from '../../forms/amenityOpenPanelBuilder.js';
import { Strings } from '../../../strings.js';

export class GiftShopOpenForSeasonView {
   static createGiftShopOpenForSeasonPanel() {
      return AmenityOpenPanelBuilder.createPanel({
         panelId: 'giftShopOpenForSeasonPanel',
         title: Strings.panelTitles.giftShopOpenForSeason,
         entityLabel: Strings.entityLabels.giftShop,
         emptyOptionLabel: Strings.placeholders.giftShop,
         idPrefix: 'giftShopOpenForSeason',
         entityFieldName: 'GiftShop',
         includeDateRange: false,
         submitId: 'submitGiftShopOpenForSeason',
         statusId: 'giftShopOpenForSeasonStatus',
      });
   }
}
