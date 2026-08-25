import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';

export const transportationStationRenderer = {
   key: 'transportationStation',

   createCard(s, index) {
      const name = s.name || 'Zoomobile Station';
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
            s.description ? `Description: ${s.description}` : '',
         ],
      });
   },
};
