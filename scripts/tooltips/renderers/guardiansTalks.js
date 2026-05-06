import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';
import { APP_STRINGS } from '../../strings.js';

export const guardiansTalkRenderer = {
   key: 'guardiansTalk',

   createCard(t, index) {
      const name = t.name || APP_STRINGS.entityLabels.guardiansTalk;
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/guardians-talks/${normalizedName}.png`,
            alt: t.name || name,
            fallbackSrc: 'images/icons/guardians-talk/guardians-talk.png',
         },
         title: { text: name },
         details: [
            APP_STRINGS.search.location(t.location),
            APP_STRINGS.tooltips.startTime(t.time_of_day),
            APP_STRINGS.tooltips.description(APP_STRINGS.tooltips.guardiansTalkDescription),
         ],
      });
   },
};
