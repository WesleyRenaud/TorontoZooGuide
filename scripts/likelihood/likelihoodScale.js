export class LikelihoodScale {
   static MIN_LIKELIHOOD = 0;
   static MAX_LIKELIHOOD = 100;

   static clampLikelihood(likelihood) {
      const numericLikelihood = Number(likelihood);

      if (!Number.isFinite(numericLikelihood)) {
         return LikelihoodScale.MIN_LIKELIHOOD;
      }

      return Math.max(
         LikelihoodScale.MIN_LIKELIHOOD,
         Math.min(LikelihoodScale.MAX_LIKELIHOOD, numericLikelihood)
      );
   }
}
