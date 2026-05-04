import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';

export const attractionRenderer = {
   key: 'attraction',

   createCard(a, index) {
      const name = a.name || 'Attraction';
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/attractions/${normalizedName}.png`,
            alt: name,
            fallbackSrc: `images/icons/attractions/${normalizedName}-open.png`,
         },
         title: { text: name },
         details: [
            a.free_with_admission ? 'Free With Admission' : 'Extra Charge',
            a.seasonal_schedule ? `Seasonal Schedule: ${a.seasonal_schedule}` : '',
            a.description ? `Description: ${a.description}` : '',
         ],
         links: a.info_link
            ? [{
               href: a.info_link,
               text: a.hyperlink_text || 'More Info',
               className: 'gift-shop-link',
            }]
            : [],
      });
   },
};
