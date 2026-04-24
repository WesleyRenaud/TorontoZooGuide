import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';

export const wildEncounterRenderer = {
   key: 'wildEncounter',

   createCard(w, index) {
      const name = w.name || 'Wild Encounter';
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/wild-encounters/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/generic-icons/wild-encounter.png',
         },
         title: { text: name },
         details: [
            w.meeting_spot || '',
            w.time_of_day || '',
         ],
         links: w.link
            ? [{
               href: w.link,
               text: 'More Info',
               className: 'gift-shop-link',
            }]
            : [],
      });
   },
};
