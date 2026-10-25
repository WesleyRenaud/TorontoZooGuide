import { LikelihoodScale } from './likelihoodScale.js';
import { LikelihoodValues } from './likelihoodValues.js';
import { StepRounder } from '../shared/stepRounder.js';
import { Strings } from '../strings.js';

export class LikelihoodPresenter {
   static DISPLAY_STEP = 5;
   static LOW_OPEN_PERCENT = 5;
   static HIGH_OPEN_PERCENT = 95;

   static LIKELIHOOD_PHRASES = Object.freeze([
      { minimum: 95, label: Strings.likelihood.veryHigh },
      { minimum: 80, label: Strings.likelihood.high },
      { minimum: 60, label: Strings.likelihood.medium },
      { minimum: 40, label: Strings.likelihood.moderate },
      { minimum: 20, label: Strings.likelihood.low },
      { minimum: 0, label: Strings.likelihood.veryLow },
   ]);

   static getLikelihoodPhrase(likelihood) {
      const value = LikelihoodScale.clampLikelihood(likelihood);

      return LikelihoodPresenter.LIKELIHOOD_PHRASES.find((phrase) => (
         value >= phrase.minimum
      ))?.label || Strings.likelihood.veryLow;
   }

   static formatDisplayedLikelihood(value) {
      const percent = LikelihoodValues.likelihoodToPercent(value);

      if (percent == null) {
         return null;
      }

      if (percent > LikelihoodScale.MIN_LIKELIHOOD && percent < LikelihoodPresenter.LOW_OPEN_PERCENT) {
         return Strings.likelihood.belowDisplayedMinimum(LikelihoodPresenter.LOW_OPEN_PERCENT);
      }

      if (percent > LikelihoodPresenter.HIGH_OPEN_PERCENT) {
         return Strings.likelihood.aboveDisplayedMaximum(LikelihoodPresenter.HIGH_OPEN_PERCENT);
      }

      const rounded = StepRounder.roundToStep(percent, LikelihoodPresenter.DISPLAY_STEP);

      return Strings.format.approximate(`${rounded}%`);
   }
}
