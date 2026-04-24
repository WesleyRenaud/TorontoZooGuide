import { clampLikelihood } from './likelihoodScale.js';

const LIKELIHOOD_PHRASES = Object.freeze([
   { minimum: 95, label: 'Very high' },
   { minimum: 80, label: 'High' },
   { minimum: 60, label: 'Medium' },
   { minimum: 40, label: 'Moderate' },
   { minimum: 20, label: 'Low' },
   { minimum: 0, label: 'Very low' },
]);

export function getLikelihoodPhrase(likelihood) {
   const value = clampLikelihood(likelihood);

   return LIKELIHOOD_PHRASES.find((phrase) => (
      value >= phrase.minimum
   ))?.label || 'Very low';
}
