import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { createTooltipCard } from './cardFactory.js';
import { normalizeStoredLink } from '../../itinerary/selectors/base/storedSelection.js';
import { MapOccurrenceTimesFormatter } from '../mapOccurrenceTimesFormatter.js';
import { APP_STRINGS } from '../../strings.js';

export const wildEncounterRenderer = {
   key: 'wildEncounter',

   createCard(w, index) {
      const name = w.name || APP_STRINGS.entityLabels.wildEncounter;
      const normalizedName = AssetKeyNormalizer.normalize(name);
      const link = normalizeStoredLink(w.link);
      const times = MapOccurrenceTimesFormatter.format(w);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/wild-encounters/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/wild-encounter/wild-encounter.png',
         },
         title: {
            text: name,
            className: link ? 'species-link' : '',
            dataset: {
               index,
               externalHref: link,
            },
         },
         details: [
            w.meeting_spot || '',
            times ? APP_STRINGS.tooltips.times(times) : '',
         ],
      });
   },
};
