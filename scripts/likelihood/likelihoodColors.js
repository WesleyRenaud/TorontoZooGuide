import { clampLikelihood } from './likelihoodScale.js';

const LIKELIHOOD_COLORS = Object.freeze([
   '#7a0000',
   '#9c0d00',
   '#be1a00',
   '#e03f00',
   '#ff6500',
   '#ff7f00',
   '#ff9900',
   '#ffb300',
   '#ffcc33',
   '#ffff33',
   '#e0ff33',
   '#c4ff33',
   '#a8ff33',
   '#8cff33',
   '#70ff33',
   '#55cc33',
   '#3abb33',
   '#2eb33a',
   '#259933',
   '#1fa544',
]);

export function likelihoodToColor(likelihood) {
   const value = clampLikelihood(likelihood);
   const index = Math.round(
      (value / 100) * (LIKELIHOOD_COLORS.length - 1)
   );

   return LIKELIHOOD_COLORS[index];
}
