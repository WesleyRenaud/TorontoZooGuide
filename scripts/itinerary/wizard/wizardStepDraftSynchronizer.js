import { VisitDateValidator } from '../../visitDates/visitDateValidator.js';
import { WizardStepConfigs } from './wizardStepConfigs.js';

export class WizardStepDraftSynchronizer {
   static resolveDateStepDraftUpdate({
      currentDate,
      wizardDate,
   } = {}) {
      if (!(currentDate instanceof Date) || !Number.isFinite(currentDate.getTime())) {
         return null;
      }

      const date = VisitDateValidator.toISODate(currentDate);

      if (!date || wizardDate === date) {
         return null;
      }

      return date;
   }

   static shouldSyncSelectionStepDraft({
      stepConfig,
      stepController,
   } = {}) {
      if (!stepConfig || typeof stepController?.getSelectionSnapshot !== 'function') {
         return false;
      }

      if (stepController.shouldSkipClosingSelectionSync?.()) {
         return false;
      }

      return true;
   }

   static isWizardDateStep(stepKey, defaultStep = WizardStepConfigs.WIZARD_DEFAULT_START_STEP) {
      return stepKey === defaultStep;
   }
}
