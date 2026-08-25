import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';
import { APP_STRINGS } from '../../strings.js';

export const transportationStationRenderer = {
   key: 'transportationStation',

   createCard(s, index) {
      const name = s.name || APP_STRINGS.tooltips.defaultTransportationStationName;
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/transportation-stations/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/zoomobile-station/zoomobile-station.png',
         },
         title: { text: name },
         details: [
            s.description ? APP_STRINGS.tooltips.description(s.description) : '',
         ],
      });
   },
};
