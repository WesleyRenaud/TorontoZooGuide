import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { StoredSelection } from '../../itinerary/selectors/base/storedSelection.js';
import { MapOccurrenceTimesFormatter } from '../mapOccurrenceTimesFormatter.js';
import { Strings } from '../../strings.js';

export class WildEncounters {
   static key = 'wildEncounter';

   static createCard(w, index) {
      const name = w.name || Strings.entityLabels.wildEncounter;
      const normalizedName = AssetKeyNormalizer.normalize(name);
      const link = StoredSelection.normalizeStoredLink(w.link);
      const times = MapOccurrenceTimesFormatter.format(w);

      return CardFactory.createTooltipCard({
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
            times ? Strings.tooltips.times(times) : '',
         ],
      });
   }
}
