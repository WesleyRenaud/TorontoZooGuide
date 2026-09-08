import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { ItemType } from '../../shared/enums/itemType.js';
import { Strings } from '../../strings.js';

export class GiftShopTooltipRenderer {
   static key = ItemType.GIFT_SHOP;

   static createCard(g, index) {
      const name = g.name || Strings.entityLabels.giftShop;
      const normalizedName = AssetKeyNormalizer.normalize(name);

      return CardFactory.createTooltipCard({
         index,
         image: {
            src: `images/details/gift-shops/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/gift-shop/gift-shop-open.png',
         },
         title: { text: name },
         details: [
            g.description ? Strings.tooltips.description(g.description) : '',
         ],
      });
   }
}
