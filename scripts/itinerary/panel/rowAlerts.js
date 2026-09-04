import { LikelihoodValues } from '../../likelihood/likelihoodValues.js';
import { APP_STRINGS } from '../../strings.js';

const { removedItems } = APP_STRINGS.itinerary;

function getLikelihoodPair(animal) {
   const beforeRaw = animal?.likelihoodBefore;
   const afterRaw = animal?.likelihoodAfter;

   const before = LikelihoodValues.likelihoodToPercent(beforeRaw);
   const after = LikelihoodValues.likelihoodToPercent(afterRaw);

   return { before, after };
}

function buildAnimalRemovalReasonLine(animal) {
   const reason = animal.removalReason ?? '';

   if (!reason) return '';

   return removedItems.unavailableReason(reason);
}

function buildAnimalVisibilityChange(animal) {
   const { before, after } = getLikelihoodPair(animal);

   if (before == null || after == null || before === after) {
      return {
         line: '',
         tone: 'default',
      };
   }

   const line = removedItems.projectedVisibilityChanged(before, after);

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

export class RowAlerts {
   static buildAnimalAlert(animal) {
      const removalLine = buildAnimalRemovalReasonLine(animal);

      if (removalLine) {
         return {
            line: removalLine,
            tone: 'default',
         };
      }

      return buildAnimalVisibilityChange(animal);
   }

   static buildAttractionRemovalReasonLine(attraction) {
      const reason = attraction.removalReason ?? '';

      if (!reason) return '';

      return removedItems.notAvailableOnDate(reason);
   }

   static buildGuardiansRemovalReasonLine(guardiansTalk) {
      const reason = guardiansTalk.removalReason ?? '';

      if (!reason) return '';

      return removedItems.notAvailableOnDate(reason);
   }

   static buildWildRemovalReasonLine(wildEncounter) {
      const reason = wildEncounter.removalReason ?? '';

      if (!reason) return '';

      return removedItems.notAvailableOnDate(reason);
   }
}
