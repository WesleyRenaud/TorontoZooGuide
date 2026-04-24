import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';

export const giftShopRenderer = {
   key: 'giftShop',

   createCard(g, index) {
      const name = g.name || 'Gift Shop';
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/gift-shops/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/generic-icons/gift-shop-open.png',
         },
         title: { text: name },
         details: [
            g.description ? `Description: ${g.description}` : '',
         ],
      });
   },
};
