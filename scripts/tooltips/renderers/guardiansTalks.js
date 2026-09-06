import { CreateSpeciesLinkTitle } from '../../animals/createSpeciesLinkTitle.js';
import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { OpenGuardiansTalkLinkedAnimal } from '../../guardians/openGuardiansTalkLinkedAnimal.js';
import { MapOccurrenceTimesFormatter } from '../mapOccurrenceTimesFormatter.js';
import { Strings } from '../../strings.js';

export class GuardiansTalks {
   static key = 'guardiansTalk';

   static createCard(t, index) {
      const name = t.name || Strings.entityLabels.guardiansTalk;
      const normalizedName = AssetKeyNormalizer.normalize(name);
      const times = MapOccurrenceTimesFormatter.format(t);
      const linkedAnimal = OpenGuardiansTalkLinkedAnimal.getGuardiansTalkLinkedAnimal(t);
      const title = linkedAnimal
         ? {
            element: CreateSpeciesLinkTitle.createSpeciesLinkTitleElement({
               text: name,
               tagName: 'strong',
               className: 'tooltip-card-title',
               dataset: {
                  index,
               },
            }),
         }
         : { text: name };

      return CardFactory.createTooltipCard({
         index,
         image: {
            src: `images/details/guardians-talks/${normalizedName}.png`,
            alt: t.name || name,
            fallbackSrc: 'images/icons/guardians-talk/guardians-talk.png',
         },
         title,
         details: [
            Strings.search.location(t.location),
            times ? Strings.tooltips.times(times) : '',
            Strings.tooltips.description(Strings.tooltips.guardiansTalkDescription),
         ],
      });
   }
}
