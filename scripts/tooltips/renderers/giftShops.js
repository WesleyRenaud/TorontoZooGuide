import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';
import { APP_STRINGS } from '../../strings.js';

export const giftShopRenderer = {
   key: 'giftShop',

   createCard(g, index) {
      const name = g.name || APP_STRINGS.entityLabels.giftShop;
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
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
   },
};
