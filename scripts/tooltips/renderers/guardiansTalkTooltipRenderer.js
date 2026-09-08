import { SpeciesLinkTitleBuilder } from '../../animals/speciesLinkTitleBuilder.js';
import { AssetKeyNormalizer } from '../../assets/assetKeyNormalizer.js';
import { CardFactory } from './cardFactory.js';
import { GuardiansTalkLinkedAnimalOpener } from '../../guardians/guardiansTalkLinkedAnimalOpener.js';
import { MapOccurrenceTimesFormatter } from '../mapOccurrenceTimesFormatter.js';
import { ItemType } from '../../shared/enums/itemType.js';
import { Strings } from '../../strings.js';

export class GuardiansTalkTooltipRenderer {
   static key = ItemType.GUARDIANS_TALK;

   static createCard(t, index) {
      const name = t.name || Strings.entityLabels.guardiansTalk;
      const normalizedName = AssetKeyNormalizer.normalize(name);
      const times = MapOccurrenceTimesFormatter.format(t);
      const linkedAnimal = GuardiansTalkLinkedAnimalOpener.getGuardiansTalkLinkedAnimal(t);
      const title = linkedAnimal
         ? {
            element: SpeciesLinkTitleBuilder.createSpeciesLinkTitleElement({
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
