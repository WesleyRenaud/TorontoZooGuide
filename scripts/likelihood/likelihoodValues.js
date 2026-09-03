import { LikelihoodScale } from './likelihoodScale.js';

/**
 * Convert a likelihood to a 0–100 percent value.
 *
 * Backend/API values are always integer percents (0–100). Some client paths
 * pass fractional values in the 0–1 range (e.g. 0.25 for 25%). Integer
 * values must not be scaled: 1 means 1%, not 100%.
 */
export class LikelihoodValues {
   static likelihoodToPercent(value) {
      if (value == null || value === '') {
         return null;
      }

      const likelihood = Number(value);

      if (!Number.isFinite(likelihood)) {
         return null;
      }

      if (Number.isInteger(likelihood)) {
         return LikelihoodScale.clampLikelihood(likelihood);
      }

      if (likelihood >= 0 && likelihood <= 1) {
         return LikelihoodScale.clampLikelihood(likelihood * 100);
      }

      return LikelihoodScale.clampLikelihood(likelihood);
   }

   static likelihoodToFraction(value) {
      const percent = LikelihoodValues.likelihoodToPercent(value);

      if (percent == null) {
         return null;
      }

      return percent / 100;
   }
}
