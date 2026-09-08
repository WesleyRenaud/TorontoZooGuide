import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { AttractionSelectorModel } from '../../itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { StoredSelectionNormalizer } from '../../itinerary/selectors/base/storedSelectionNormalizer.js';
import { ItemType } from '../../shared/enums/itemType.js';
import { Strings } from '../../strings.js';

export class AttractionTooltipRenderer {
   static key = ItemType.ATTRACTION;

   static createCard(a, index) {
      const name = a.name || Strings.entityLabels.attraction;
      const normalizedName = AssetKeyNormalizer.normalize(name);
      const infoLink = StoredSelectionNormalizer.normalizeStoredLink(a.info_link);

      return CardFactory.createTooltipCard({
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
            AttractionSelectorModel.getAttractionSubtitle(a),
            a.seasonal_schedule
               ? Strings.tooltips.seasonalSchedule(a.seasonal_schedule)
               : '',
            a.description ? Strings.tooltips.description(a.description) : '',
         ],
      });
   }
}
