import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { Strings } from '../../strings.js';

export class TransportationStations {
   static key = 'transportationStation';

   static createCard(s, index) {
      const name = s.name || Strings.tooltips.defaultTransportationStationName;
      const normalizedName = AssetKeyNormalizer.normalize(name);

      return CardFactory.createTooltipCard({
         index,
         image: {
            src: `images/details/transportation-stations/${normalizedName}.png`,
            alt: name,
            fallbackSrc: 'images/icons/zoomobile-station/zoomobile-station.png',
         },
         title: { text: name },
         details: [
            s.description ? Strings.tooltips.description(s.description) : '',
         ],
      });
   }
}
