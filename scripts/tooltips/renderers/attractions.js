import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { createTooltipCard } from './cardFactory.js';
import { getAttractionSubtitle } from '../../itinerary/selectors/attractionSelector/model.js';
import { normalizeStoredLink } from '../../itinerary/selectors/base/storedSelection.js';
import { APP_STRINGS } from '../../strings.js';

export const attractionRenderer = {
   key: 'attraction',

   createCard(a, index) {
      const name = a.name || APP_STRINGS.entityLabels.attraction;
      const normalizedName = AssetKeyNormalizer.normalize(name);
      const infoLink = normalizeStoredLink(a.info_link);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/attractions/${normalizedName}.png`,
            alt: name,
            fallbackSrc: `images/icons/attractions/${normalizedName}-open.png`,
         },
         title: {
            text: name,
            className: infoLink ? 'species-link' : '',
            dataset: {
               index,
               externalHref: infoLink,
            },
         },
         details: [
            getAttractionSubtitle(a),
            a.seasonal_schedule
               ? APP_STRINGS.tooltips.seasonalSchedule(a.seasonal_schedule)
               : '',
            a.description ? APP_STRINGS.tooltips.description(a.description) : '',
         ],
      });
   },
};
