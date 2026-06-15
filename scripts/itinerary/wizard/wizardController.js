import { syncItineraryAnimalDraftFromItinerary } from '../draftStorage.js';
import { showItineraryConfirmPopup } from '../../itinerary/panel/components/confirmPopup.js';
import { createItineraryDateSelectorController } from '../../itinerary/selectors/dateSelector.js';
import { getItinerary } from '../itineraryService.js';
import { createItineraryWizardState } from './state.js';
import { APP_STRINGS } from '../../strings.js';
import { resolveEarliestSelectableVisitDateNoon } from '../visitDateEarliest.js';
import { buildWizardDraft } from './wizardDraft.js';
import { finalizeItineraryWizard } from './wizardFinalizer.js';
import {
   buildSelectionStepHandlers,
   resolveWizardStartStep,
   WIZARD_DEFAULT_START_STEP,
   WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY,
} from './wizardStepConfigs.js';
import {
   isWizardDateStep,
   resolveDateStepDraftUpdate,
   shouldSyncSelectionStepDraft,
} from './wizardStepDraftSync.js';

async function loadDefaultSelectionStepConfigs() {
   const { buildWizardSelectionStepConfigs } = await import(
      './wizardSelectionStepFactories.js'
   );

   return buildWizardSelectionStepConfigs();
}

function clearWizard(mountEl) {
   mountEl?.replaceChildren();
}

function closeWizard(mountEl, onDone) {
   clearWizard(mountEl);
   onDone?.();
}

export async function openItineraryWizard({
   mountEl,
   startAt = WIZARD_DEFAULT_START_STEP,
   onDone,
   deps = {},
} = {}) {
   const {
      loadItinerary = getItinerary,
      resolveEarliestVisitDate = resolveEarliestSelectableVisitDateNoon,
      createWizardState = createItineraryWizardState,
      createDateStepController = createItineraryDateSelectorController,
      finalizeWizard = finalizeItineraryWizard,
      showConfirmPopup = showItineraryConfirmPopup,
      syncAnimalDraft = syncItineraryAnimalDraftFromItinerary,
      loadSelectionStepConfigs = loadDefaultSelectionStepConfigs,
      selectionStepConfigs = null,
   } = deps;

   if (!mountEl) {
      return;
   }

   const resolvedSelectionStepConfigs = selectionStepConfigs
      ?? await loadSelectionStepConfigs();

   const existing = await loadItinerary();

   if (existing?.isActive) {
      syncAnimalDraft(existing);
   }

   const earliestVisitNoon = await resolveEarliestVisitDate();
   const wizard = createWizardState(existing ?? {});
   const { state: wizardState } = wizard;

   const wizardSteps = {};
   let activeStepKey = WIZARD_DEFAULT_START_STEP;

   function showStep(stepKey) {
      activeStepKey = stepKey;
      return wizardSteps[stepKey]?.show();
   }

   function updateSelection(selectionKey, value, options = {}) {
      wizard.updateSelection(selectionKey, value, options);
   }

   function handleFinishDone(savedItinerary) {
      wizard.consumePendingValidation();
      onDone?.(savedItinerary);
   }

   function finish(override = {}, options = {}) {
      return finalizeWizard(
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

   function applyWizardDate(date) {
      wizard.applyValidationResult(date, null);
   }

   function syncDateStepDraft() {
      const nextDate = resolveDateStepDraftUpdate({
         currentDate: wizardSteps.date?.getDate?.(),
         wizardDate: wizardState.date,
      });

      if (!nextDate) {
         return;
      }

      applyWizardDate(nextDate);
   }

   async function syncSelectionStepDraft(stepKey) {
      const activeConfig = WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY[stepKey];
      const activeController = wizardSteps[stepKey];

      if (!shouldSyncSelectionStepDraft({
         stepConfig: activeConfig,
         stepController: activeController,
      })) {
         return;
      }

      const selection = await activeController.getSelectionSnapshot();

      updateSelection(activeConfig.selectionKey, selection, {
         preserveOnInvalid: activeConfig.preserveOnInvalid,
      });
   }

   async function syncActiveStepDraft() {
      if (isWizardDateStep(activeStepKey)) {
         syncDateStepDraft();
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

      showConfirmPopup({
         title: APP_STRINGS.itinerary.confirmation.saveChangesTitle,
         message: APP_STRINGS.itinerary.confirmation.saveChangesMessage,
         confirmText: APP_STRINGS.actions.save,
         cancelText: APP_STRINGS.itinerary.actions.discard,
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
            ? (value) => {
               updateSelection(config.selectionKey, value, {
                  preserveOnInvalid: config.preserveOnInvalid,
               });
               showStep(config.prevStepKey);
            }
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

   resolvedSelectionStepConfigs.forEach(createSelectionStepController);

   function handleDateNext(date) {
      applyWizardDate(date);
      showStep('regions');
   }

   async function handleDateFinish(date) {
      applyWizardDate(date);
      await finish({ date }, { allowEmpty: true });
   }

   wizardSteps.date = createDateStepController({
      mountEl,
      earliestSelectableDate: earliestVisitNoon,
      onClose: handleClose,
      onSave: handleDateNext,
      onFinish: handleDateFinish,
   });

   return showStep(resolveWizardStartStep(startAt));
}
