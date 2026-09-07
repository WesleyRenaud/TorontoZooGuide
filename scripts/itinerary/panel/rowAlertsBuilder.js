import { LikelihoodValues } from '../../likelihood/likelihoodValues.js';
import { Strings } from '../../strings.js';

export class RowAlertsBuilder {
   static getLikelihoodPair(animal) {
      const beforeRaw = animal?.likelihoodBefore;
      const afterRaw = animal?.likelihoodAfter;

      const before = LikelihoodValues.likelihoodToPercent(beforeRaw);
      const after = LikelihoodValues.likelihoodToPercent(afterRaw);

      return { before, after };
   }

   static buildAnimalRemovalReasonLine(animal) {
      const reason = animal.removalReason ?? '';

      if (!reason) return '';

      return Strings.itinerary.removedItems.unavailableReason(reason);
   }

   static buildAnimalVisibilityChange(animal) {
      const { before, after } = RowAlertsBuilder.getLikelihoodPair(animal);

      if (before == null || after == null || before === after) {
         return {
            line: '',
            tone: 'default',
         };
      }

      const line = Strings.itinerary.removedItems.projectedVisibilityChanged(before, after);

      if (after < before) {
         return {
            line,
            tone: 'default',
         };
      }

      return {
         line,
         tone: 'positive',
      };
   }
}
