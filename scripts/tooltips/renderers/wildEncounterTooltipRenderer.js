import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { StoredSelectionNormalizer } from '../../itinerary/selectors/base/storedSelectionNormalizer.js';
import { MapOccurrenceTimesFormatter } from '../mapOccurrenceTimesFormatter.js';
import { ItemType } from '../../shared/enums/itemType.js';
import { Strings } from '../../strings.js';

export class WildEncounterTooltipRenderer {
   static key = ItemType.WILD_ENCOUNTER;

   static createCard(w, index) {
      const name = w.name || Strings.entityLabels.wildEncounter;
      const normalizedName = AssetKeyNormalizer.normalize(name);
      const link = StoredSelectionNormalizer.normalizeStoredLink(w.link);
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
