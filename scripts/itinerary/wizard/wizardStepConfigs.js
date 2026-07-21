export const WIZARD_DEFAULT_START_STEP = 'date';

export const WIZARD_SELECTION_STEP_DEFINITIONS = Object.freeze([
   {
      stepKey: 'wildEncounters',
      selectionKey: 'wildEncounters',
      prevStepKey: 'guardiansTalks',
   },
   {
      stepKey: 'guardiansTalks',
      selectionKey: 'guardiansTalks',
      prevStepKey: 'attractions',
      nextStepKey: 'wildEncounters',
   },
   {
      stepKey: 'attractions',
      selectionKey: 'attractions',
      prevStepKey: 'animals',
      nextStepKey: 'guardiansTalks',
   },
   {
      stepKey: 'animals',
      selectionKey: 'animals',
      prevStepKey: 'regions',
      nextStepKey: 'attractions',
   },
   {
      stepKey: 'regions',
      selectionKey: 'animals',
      prevStepKey: 'date',
      nextStepKey: 'animals',
      preserveOnInvalid: true,
   },
]);

export const WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY = Object.freeze(
   Object.fromEntries(
      WIZARD_SELECTION_STEP_DEFINITIONS.map((definition) => [
         definition.stepKey,
         definition,
      ])
   )
);

export function resolveWizardStartStep(
   startAt,
   configsByKey = WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY,
   defaultStep = WIZARD_DEFAULT_START_STEP
) {
   if (startAt === defaultStep) {
      return defaultStep;
   }

   return Object.prototype.hasOwnProperty.call(configsByKey, startAt)
      ? startAt
      : defaultStep;
}

export function buildSelectionStepHandlers({
   selectionKey,
   preserveOnInvalid = false,
   updateSelection,
   showNextStep = null,
   finish,
} = {}) {
   return {
      onNext: showNextStep
         ? (value) => {
            updateSelection(selectionKey, value, { preserveOnInvalid });
            showNextStep();
         }
         : undefined,
      onFinish: (value) => {
         if (value == null) {
            void finish();
            return;
         }

         void finish({ [selectionKey]: value });
      },
   };
}
