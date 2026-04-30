import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createTooltipCard } from './cardFactory.js';

export const pavilionRenderer = {
   key: 'pavilion',

   createCard(p, index) {
      const name = p.name || 'Pavilion';
      const normalizedName = normalizeAssetKey(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/pavilions/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/pavilion/pavilion-open.png',
         },
         title: { text: name },
         details: [
            p.region ? `Region: ${p.region}` : '',
            p.description ? `Description: ${p.description}` : '',
         ],
      });
   },
};
