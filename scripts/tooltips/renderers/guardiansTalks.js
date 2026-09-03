import { createSpeciesLinkTitleElement } from '../../animals/createSpeciesLinkTitle.js';
import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { createTooltipCard } from './cardFactory.js';
import { getGuardiansTalkLinkedAnimal } from '../../guardians/openGuardiansTalkLinkedAnimal.js';
import { MapOccurrenceTimesFormatter } from '../mapOccurrenceTimesFormatter.js';
import { APP_STRINGS } from '../../strings.js';

export const guardiansTalkRenderer = {
   key: 'guardiansTalk',

   createCard(t, index) {
      const name = t.name || APP_STRINGS.entityLabels.guardiansTalk;
      const normalizedName = AssetKeyNormalizer.normalize(name);
      const times = MapOccurrenceTimesFormatter.format(t);
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
