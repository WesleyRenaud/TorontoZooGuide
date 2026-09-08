import { RowAlertsBuilder } from './rowAlertsBuilder.js';
import { Strings } from '../../strings.js';

export class RowAlertPresenter {
   static buildAnimalAlert(animal) {
      const removalLine = RowAlertsBuilder.buildAnimalRemovalReasonLine(animal);

      if (removalLine) {
         return {
            line: removalLine,
            tone: 'default',
         };
      }

      return RowAlertsBuilder.buildAnimalVisibilityChange(animal);
   }

   static buildAttractionRemovalReasonLine(attraction) {
      const reason = attraction.removalReason ?? '';

      if (!reason) return '';

      return Strings.itinerary.removedItems.notAvailableOnDate(reason);
   }

   static buildGuardiansRemovalReasonLine(guardiansTalk) {
      const reason = guardiansTalk.removalReason ?? '';

      if (!reason) return '';

      return Strings.itinerary.removedItems.notAvailableOnDate(reason);
   }

   static buildWildRemovalReasonLine(wildEncounter) {
      const reason = wildEncounter.removalReason ?? '';

      if (!reason) return '';

      return Strings.itinerary.removedItems.notAvailableOnDate(reason);
   }
}
