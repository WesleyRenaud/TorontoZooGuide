import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';

export const zoomobileStationRenderer = {
   key: 'zoomobileStation',

   createCard(s, index) {
      const name = s.name || 'Zoomobile Station';
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/zoomobile-stations/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/generic-icons/zoomobile-station.png',
         },
         title: { text: name },
         details: [
            s.description ? `Description: ${s.description}` : '',
         ],
      });
   },
};
