import { toISODate } from '../../visitDates/visitDateRules.js';
import { WIZARD_DEFAULT_START_STEP } from './wizardStepConfigs.js';

export function resolveDateStepDraftUpdate({
   currentDate,
   wizardDate,
} = {}) {
   if (!(currentDate instanceof Date) || !Number.isFinite(currentDate.getTime())) {
      return null;
   }

   const date = toISODate(currentDate);

   if (!date || wizardDate === date) {
      return null;
   }

   return date;
}

export function shouldSyncSelectionStepDraft({
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

export function isWizardDateStep(stepKey, defaultStep = WIZARD_DEFAULT_START_STEP) {
   return stepKey === defaultStep;
}
