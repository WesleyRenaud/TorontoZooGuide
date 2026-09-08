import { WarningBuilder } from '../../../assets/warningBuilder.js';
import { Strings } from '../../../strings.js';

export class AnimalSelectorRendererHelper {
   static createLikelihoodWarning(level) {
      if (!level) {
         return null;
      }

      const warning = document.createElement('span');
      warning.className = `itin-likelihood-warning ${level}`;
      warning.appendChild(WarningBuilder.createWarningIcon());
      warning.title = level === 'low'
         ? Strings.itinerary.selectors.lowVisibilityHint
         : Strings.itinerary.confirmation.animalMayBeOffDisplay;

      return warning;
   }
}
