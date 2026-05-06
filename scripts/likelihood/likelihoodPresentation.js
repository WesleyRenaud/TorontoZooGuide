import { clampLikelihood } from './likelihoodScale.js';
import { APP_STRINGS } from '../strings.js';

const LIKELIHOOD_PHRASES = Object.freeze([
   { minimum: 95, label: APP_STRINGS.likelihood.veryHigh },
   { minimum: 80, label: APP_STRINGS.likelihood.high },
   { minimum: 60, label: APP_STRINGS.likelihood.medium },
   { minimum: 40, label: APP_STRINGS.likelihood.moderate },
   { minimum: 20, label: APP_STRINGS.likelihood.low },
   { minimum: 0, label: APP_STRINGS.likelihood.veryLow },
]);

export function getLikelihoodPhrase(likelihood) {
   const value = clampLikelihood(likelihood);

   return LIKELIHOOD_PHRASES.find((phrase) => (
      value >= phrase.minimum
   ))?.label || APP_STRINGS.likelihood.veryLow;
}
