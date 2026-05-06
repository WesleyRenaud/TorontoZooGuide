import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';
import { APP_STRINGS } from '../../strings.js';

export const restaurantRenderer = {
   key: 'restaurant',

   createCard(r, index) {
      const name = r.name || APP_STRINGS.entityLabels.restaurant;
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
               ? APP_STRINGS.search.location(r.sub_location)
               : r.location
                  ? APP_STRINGS.search.location(r.location)
                  : '',
            r.description ? APP_STRINGS.tooltips.description(r.description) : '',
         ],
         links: r.menu_link
            ? [{
               href: r.menu_link,
               text: APP_STRINGS.tooltips.menu,
               className: 'restaurant-menu-link',
            }]
            : [],
      });
   },
};
