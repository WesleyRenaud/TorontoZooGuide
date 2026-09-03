import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { createTooltipCard } from './cardFactory.js';
import { APP_STRINGS } from '../../strings.js';

export const pavilionRenderer = {
   key: 'pavilion',

   createCard(p, index) {
      const name = p.name || APP_STRINGS.entityLabels.pavilion;
      const normalizedName = AssetKeyNormalizer.normalize(name);

      return createTooltipCard({
         index,
         image: {
            src: `images/details/pavilions/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/pavilion/pavilion-open.png',
         },
         title: { text: name },
         details: [
            p.region ? APP_STRINGS.search.region(p.region) : '',
            p.description ? APP_STRINGS.tooltips.description(p.description) : '',
         ],
      });
   },
};
