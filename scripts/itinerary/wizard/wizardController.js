import { createItineraryDateSelectorController } from '../../itinerary/selectors/dateSelector.js';
import { createItineraryRegionSelectorController } from '../../itinerary/selectors/regionSelector.js';
import { createItineraryAnimalSelectorController } from '../../itinerary/selectors/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../../itinerary/selectors/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../../itinerary/selectors/guardiansTalkSelector.js';
import { createItineraryWildEncounterSelectorController } from '../../itinerary/selectors/wildEncounterSelector.js';
import { toISODate } from '../../visitDates/visitDateRules.js';

import { showItineraryConfirmPopup } from '../../itinerary/panel/components/confirmPopup.js';

import { getItinerary } from '../itineraryService.js';
import { finalizeItineraryWizard } from './wizardFinalizer.js';
import { validateItineraryDraft } from './draftValidator.js';
import { createItineraryWizardState } from './state.js';
import { showWizardValidationPopupIfNeeded } from './validationPopup.js';

const DEFAULT_START_STEP = 'date';

const SELECTION_STEP_CONFIGS = Object.freeze([
   {
      stepKey: 'wildEncounters',
      selectionKey: 'wildEncounters',
      factory: createItineraryWildEncounterSelectorController,
      prevStepKey: 'guardiansTalks',
   },
   {
      stepKey: 'guardiansTalks',
      selectionKey: 'guardiansTalks',
      factory: createItineraryGuardiansTalkSelectorController,
      prevStepKey: 'attractions',
      nextStepKey: 'wildEncounters',
   },
   {
      stepKey: 'attractions',
      selectionKey: 'attractions',
      factory: createItineraryAttractionSelectorController,
      prevStepKey: 'animals',
      nextStepKey: 'guardiansTalks',
   },
   {
      stepKey: 'animals',
      selectionKey: 'animals',
      factory: createItineraryAnimalSelectorController,
      prevStepKey: 'regions',
      nextStepKey: 'attractions',
   },
   {
      stepKey: 'regions',
      selectionKey: 'animals',
      factory: createItineraryRegionSelectorController,
      prevStepKey: 'date',
      nextStepKey: 'animals',
      preserveOnInvalid: true,
   },
]);

const SELECTION_STEP_CONFIGS_BY_KEY = Object.freeze(
   Object.fromEntries(
      SELECTION_STEP_CONFIGS.map((config) => [config.stepKey, config])
   )
);

function clearWizard(mountEl) {
   mountEl?.replaceChildren();
}

function closeWizard(mountEl, onDone) {
   clearWizard(mountEl);
   onDone?.();
}

function buildWizardDraft(wizardState, override = {}) {
   return {
      date: override.date ?? wizardState.date,
      animals: override.animals ?? wizardState.animals,
      attractions: override.attractions ?? wizardState.attractions,
      guardiansTalks: override.guardiansTalks ?? wizardState.guardiansTalks,
      wildEncounters: override.wildEncounters ?? wizardState.wildEncounters,
   };
}

function buildSelectionStepHandlers({
   selectionKey,
   preserveOnInvalid = false,
   wizardState,
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
         updateSelection(selectionKey, value, { preserveOnInvalid });
         void finish({ [selectionKey]: wizardState[selectionKey] });
      },
   };
}

function scheduleWizardValidationPopup({
   mountEl,
   pendingValidation,
   onViewAlternatives,
} = {}) {
   requestAnimationFrame(() => {
      showWizardValidationPopupIfNeeded({
         mountEl,
         pendingValidation,
         onViewAlternatives,
      });
   });
}

function resolveStartStep(startAt) {
   if (startAt === DEFAULT_START_STEP) {
      return DEFAULT_START_STEP;
   }

   return Object.prototype.hasOwnProperty.call(
      SELECTION_STEP_CONFIGS_BY_KEY,
      startAt
   )
      ? startAt
      : DEFAULT_START_STEP;
}

export async function openItineraryWizard({
   mountEl,
   startAt = DEFAULT_START_STEP,
   onDone,
} = {}) {
   if (!mountEl) {
      return;
   }

   const existing = await getItinerary();
   const wizard = createItineraryWizardState(existing ?? {});
   const { state: wizardState } = wizard;

   const wizardSteps = {};
   let activeStepKey = DEFAULT_START_STEP;

   function showStep(stepKey) {
      activeStepKey = stepKey;
      return wizardSteps[stepKey]?.show();
   }

   function reopenWizardAtStep(stepKey) {
      openItineraryWizard({
         mountEl,
         startAt: stepKey,
         onDone,
      });
   }

   function updateSelection(selectionKey, value, options = {}) {
      wizard.updateSelection(selectionKey, value, options);
   }

   function handleFinishDone() {
      onDone?.();

      const pendingValidation = wizard.consumePendingValidation();

      scheduleWizardValidationPopup({
         mountEl,
         pendingValidation,
         onViewAlternatives: reopenWizardAtStep,
      });
   }

   function finish(override = {}, options = {}) {
      return finalizeItineraryWizard(
         buildWizardDraft(wizardState, override),
         mountEl,
         {
            allowEmpty: wizard.allowEmptyFinish(options.allowEmpty),
            onDone: handleFinishDone,
         }
      );
   }

   function discardAndClose() {
      wizard.discardChanges();
      closeWizard(mountEl, onDone);
   }

   async function validateAndApplyDate(date, dateObj) {
      const result = await validateItineraryDraft({
         date,
         dateObj,
         draft: buildWizardDraft(wizardState, { date }),
      });

      wizard.applyValidationResult(date, result);
   }

   async function syncDateStepDraft() {
      const currentDate = wizardSteps.date?.getDate?.();

      if (!(currentDate instanceof Date) || !Number.isFinite(currentDate.getTime())) {
         return;
      }

      const date = toISODate(currentDate);

      if (!date || wizardState.date === date) {
         return;
      }

      await validateAndApplyDate(date, currentDate);
   }

   async function syncSelectionStepDraft(stepKey) {
      const activeConfig = SELECTION_STEP_CONFIGS_BY_KEY[stepKey];
      const activeController = wizardSteps[stepKey];

      if (
         !activeConfig
         || typeof activeController?.getSelectionSnapshot !== 'function'
      ) {
         return;
      }

      const selection = await activeController.getSelectionSnapshot();

      updateSelection(activeConfig.selectionKey, selection, {
         preserveOnInvalid: activeConfig.preserveOnInvalid,
      });
   }

   async function syncActiveStepDraft() {
      if (activeStepKey === DEFAULT_START_STEP) {
         await syncDateStepDraft();
         return;
      }

      await syncSelectionStepDraft(activeStepKey);
   }

   async function handleClose() {
      await syncActiveStepDraft();

      if (!wizard.hasUnsavedChanges()) {
         closeWizard(mountEl, onDone);
         return;
      }

      showItineraryConfirmPopup({
         title: 'Save Changes?',
         message: 'You have unsaved itinerary changes. Would you like to save them before closing?',
         confirmText: 'Save',
         cancelText: 'Discard',
         onConfirm: () => {
            void finish();
         },
         onCancel: discardAndClose,
      });
   }

   function createSelectionStepController(config = {}) {
      wizardSteps[config.stepKey] = config.factory({
         mountEl,
         onClose: handleClose,
         onPrev: config.prevStepKey
            ? () => showStep(config.prevStepKey)
            : undefined,
         ...buildSelectionStepHandlers({
            selectionKey: config.selectionKey,
            preserveOnInvalid: config.preserveOnInvalid,
            wizardState,
            updateSelection,
            showNextStep: config.nextStepKey
               ? () => showStep(config.nextStepKey)
               : null,
            finish,
         }),
      });
   }

   SELECTION_STEP_CONFIGS.forEach(createSelectionStepController);

   async function handleDateSelection(date, dateObj) {
      await validateAndApplyDate(date, dateObj);
      showStep('regions');
   }

   wizardSteps.date = createItineraryDateSelectorController({
      mountEl,
      onClose: handleClose,
      onSave: handleDateSelection,
      onFinish: handleDateSelection,
   });

   return showStep(resolveStartStep(startAt));
}
