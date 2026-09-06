import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { Strings } from '../../strings.js';

export class Restaurants {
   static key = 'restaurant';

   static createCard(r, index) {
      const name = r.name || Strings.entityLabels.restaurant;
      const normalizedName = AssetKeyNormalizer.normalize(name);

      return CardFactory.createTooltipCard({
         index,
         image: {
            src: `images/details/restaurants/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/restaurant/restaurant-open.png',
         },
         title: { text: name },
         details: [
            r.sub_location
               ? Strings.search.location(r.sub_location)
               : r.location
                  ? Strings.search.location(r.location)
                  : '',
            r.description ? Strings.tooltips.description(r.description) : '',
         ],
         links: r.menu_link
            ? [{
               href: r.menu_link,
               text: Strings.tooltips.menu,
               className: 'restaurant-menu-link',
            }]
            : [],
      });
   }
}
