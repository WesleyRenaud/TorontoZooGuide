import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { Strings } from '../../strings.js';

export class Pavilions {
   static key = 'pavilion';

   static createCard(p, index) {
      const name = p.name || Strings.entityLabels.pavilion;
      const normalizedName = AssetKeyNormalizer.normalize(name);

      return CardFactory.createTooltipCard({
         index,
         image: {
            src: `images/details/pavilions/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/pavilion/pavilion-open.png',
         },
         title: { text: name },
         details: [
            p.region ? Strings.search.region(p.region) : '',
            p.description ? Strings.tooltips.description(p.description) : '',
         ],
      });
   }
}
