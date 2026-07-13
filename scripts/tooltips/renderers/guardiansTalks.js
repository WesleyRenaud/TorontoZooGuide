import { createSpeciesLinkTitleElement } from '../../animals/createSpeciesLinkTitle.js';
import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';
import { formatMapOccurrenceTimes } from '../formatMapOccurrenceTimes.js';
import { getGuardiansTalkLinkedAnimal } from '../../guardians/openGuardiansTalkLinkedAnimal.js';
import { APP_STRINGS } from '../../strings.js';

export const guardiansTalkRenderer = {
   key: 'guardiansTalk',

   createCard(t, index) {
      const name = t.name || APP_STRINGS.entityLabels.guardiansTalk;
      const normalizedName = normalizeAssetKey(name);
      const times = formatMapOccurrenceTimes(t);
      const linkedAnimal = getGuardiansTalkLinkedAnimal(t);
      const title = linkedAnimal
         ? {
            element: createSpeciesLinkTitleElement({
               text: name,
               tagName: 'strong',
               className: 'tooltip-card-title',
               dataset: {
                  index,
               },
            }),
         }
         : { text: name };

      return createTooltipCard({
         index,
         image: {
            src: `images/details/guardians-talks/${normalizedName}.png`,
            alt: t.name || name,
            fallbackSrc: 'images/icons/guardians-talk/guardians-talk.png',
         },
         title,
         details: [
            APP_STRINGS.search.location(t.location),
            times ? APP_STRINGS.tooltips.times(times) : '',
            APP_STRINGS.tooltips.description(APP_STRINGS.tooltips.guardiansTalkDescription),
         ],
      });
   },
};
