import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { APP_STRINGS } from '../../strings.js';

export class GiftShops {
   static key = 'giftShop';

   static createCard(g, index) {
      const name = g.name || APP_STRINGS.entityLabels.giftShop;
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
            g.description ? APP_STRINGS.tooltips.description(g.description) : '',
         ],
      });
   }
}
