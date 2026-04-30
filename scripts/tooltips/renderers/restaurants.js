import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';

export const restaurantRenderer = {
   key: 'restaurant',

   createCard(r, index) {
      const name = r.name || 'Restaurant';
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/restaurants/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/restaurant/restaurant-open.png',
         },
         title: { text: name },
         details: [
            r.sub_location
               ? `Location: ${r.sub_location}`
               : r.location
                  ? `Location: ${r.location}`
                  : '',
            r.description ? `Description: ${r.description}` : '',
         ],
         links: r.menu_link
            ? [{
               href: r.menu_link,
               text: 'MENU',
               className: 'restaurant-menu-link',
            }]
            : [],
      });
   },
};
