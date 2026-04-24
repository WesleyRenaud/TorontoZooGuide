export const MIN_LIKELIHOOD = 0;
export const MAX_LIKELIHOOD = 100;

export function clampLikelihood(likelihood) {
   const numericLikelihood = Number(likelihood);

   if (!Number.isFinite(numericLikelihood)) {
      return MIN_LIKELIHOOD;
   }

   return Math.max(
      MIN_LIKELIHOOD,
      Math.min(MAX_LIKELIHOOD, numericLikelihood)
   );
}
