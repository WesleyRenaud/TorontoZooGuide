import { LikelihoodScale } from './likelihoodScale.js';
import { Strings } from '../strings.js';

const LIKELIHOOD_PHRASES = Object.freeze([
   { minimum: 95, label: Strings.likelihood.veryHigh },
   { minimum: 80, label: Strings.likelihood.high },
   { minimum: 60, label: Strings.likelihood.medium },
   { minimum: 40, label: Strings.likelihood.moderate },
   { minimum: 20, label: Strings.likelihood.low },
   { minimum: 0, label: Strings.likelihood.veryLow },
]);

export class LikelihoodPresentation {
   static getLikelihoodPhrase(likelihood) {
      const value = LikelihoodScale.clampLikelihood(likelihood);

      return LIKELIHOOD_PHRASES.find((phrase) => (
         value >= phrase.minimum
      ))?.label || Strings.likelihood.veryLow;
   }
}
