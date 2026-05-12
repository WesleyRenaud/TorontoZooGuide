import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';
import { APP_STRINGS } from '../../strings.js';

export const wildEncounterRenderer = {
   key: 'wildEncounter',

   createCard(w, index) {
      const name = w.name || APP_STRINGS.entityLabels.wildEncounter;
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/wild-encounters/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/wild-encounter/wild-encounter.png',
         },
         title: { text: name },
         details: [
            w.meeting_spot || '',
            w.start_time || '',
         ],
         links: w.link
            ? [{
               href: w.link,
               text: APP_STRINGS.common.moreInfo,
               className: 'gift-shop-link',
            }]
            : [],
      });
   },
};
