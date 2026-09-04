import { DraftStorage } from '../draftStorage.js';
import { FilterDraftExcludingWarningFixedTimeItems } from './filterDraftExcludingWarningFixedTimeItems.js';
import { showItineraryConfirmPopup } from '../../itinerary/panel/components/confirmPopup.js';
import { createItineraryDateSelectorController } from '../../itinerary/selectors/dateSelector.js';
import { ItineraryConfirmationResult } from '../itineraryConfirmationResult.js';
import {
   getItinerary,
   isItineraryEmpty,
} from '../itineraryService.js';
import { ItineraryShape } from '../itineraryShape.js';
import { SectionConfigs } from '../panel/sectionConfigs.js';
import { createItineraryWizardState } from './state.js';
import { APP_STRINGS } from '../../strings.js';
import { VisitDateEarliest } from '../visitDateEarliest.js';
import { WizardDraft } from './wizardDraft.js';
import { WizardFinalizeDecisions } from './wizardFinalizeDecisions.js';
import { finalizeItineraryWizard } from './wizardFinalizer.js';
import { WizardStepConfigs } from './wizardStepConfigs.js';
import { WizardStepDraftSync } from './wizardStepDraftSync.js';

async function loadDefaultSelectionStepConfigs() {
   const { buildWizardSelectionStepConfigs } = await import(
      './wizardSelectionStepFactories.js'
   );

   return buildWizardSelectionStepConfigs();
}

function clearWizard(mountEl) {
   mountEl?.replaceChildren();
}

function closeWizard(mountEl) {
   clearWizard(mountEl);
}

export async function openItineraryWizard({
   mountEl,
   startAt = WizardStepConfigs.WIZARD_DEFAULT_START_STEP,
   deps = {},
} = {}) {
   const {
      loadItinerary = getItinerary,
      resolveEarliestVisitDate = VisitDateEarliest.resolveEarliestSelectableVisitDateNoon,
      createWizardState = createItineraryWizardState,
      createDateStepController = createItineraryDateSelectorController,
      finalizeWizard = finalizeItineraryWizard,
      showConfirmPopup = showItineraryConfirmPopup,
      syncAnimalDraft = DraftStorage.syncItineraryAnimalDraftFromItinerary,
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
   else if (!existing || isItineraryEmpty(existing)) {
      DraftStorage.clearItinerarySelectionStorage();
   }

   const earliestVisitNoon = await resolveEarliestVisitDate();
   const wizard = createWizardState(existing ?? {});
   const { state: wizardState } = wizard;

   const wizardSteps = {};
   let activeStepKey = WizardStepConfigs.WIZARD_DEFAULT_START_STEP;

   function showStep(stepKey) {
      activeStepKey = stepKey;
      return wizardSteps[stepKey]?.show();
   }

   function updateSelection(selectionKey, value, options = {}) {
      wizard.updateSelection(selectionKey, value, options);
   }

   function handleFinishDone() {
      wizard.consumePendingValidation();
   }

   function applyFinishOverride(override = {}) {
      if (override.date != null) {
         applyWizardDate(override.date);
      }

      ItineraryShape.ITINERARY_ITEM_KEYS.forEach((selectionKey) => {
         if (!Object.prototype.hasOwnProperty.call(override, selectionKey)) {
            return;
         }

         // null means the active step skipped rebuilding (unchanged selection).
         if (override[selectionKey] == null) {
            return;
         }

         updateSelection(selectionKey, override[selectionKey]);
      });
   }

   async function finish(override = {}, options = {}) {
      await syncActiveStepDraft();
      applyFinishOverride(override);

      if (
         !wizard.hasUnsavedChanges()
         && !WizardFinalizeDecisions.shouldBlockEmptyFinish(
            WizardDraft.buildWizardDraft(wizardState),
            wizard.allowEmptyFinish(options.allowEmpty)
         )
      ) {
         // Clear the overlay only. Do not remount the day planner — that jumps
         // scroll. Saved itinerary content is already on the page.
         clearWizard(mountEl);
         handleFinishDone();
         return existing;
      }

      const result = await finalizeWizard(
         WizardDraft.buildWizardDraft(wizardState),
         mountEl,
         {
            allowEmpty: wizard.allowEmptyFinish(options.allowEmpty),
            onDone: handleFinishDone,
         }
      );

      if (ItineraryConfirmationResult.isItineraryConfirmationCancelled(result)) {
         const nextSelections = FilterDraftExcludingWarningFixedTimeItems.filterDraftExcludingWarningFixedTimeItems(
            wizardState,
            result.issues
         );

         SectionConfigs.SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS.forEach((selectionKey) => {
            updateSelection(selectionKey, nextSelections[selectionKey]);
         });
         showStep(activeStepKey);
      }

      return result;
   }

   function discardAndClose() {
      wizard.discardChanges();
      closeWizard(mountEl);
   }

   function applyWizardDate(date) {
      wizard.applyValidationResult(date, null);
   }

   function syncDateStepDraft() {
      const nextDate = WizardStepDraftSync.resolveDateStepDraftUpdate({
         currentDate: wizardSteps.date?.getDate?.(),
         wizardDate: wizardState.date,
      });

      if (!nextDate) {
         return;
      }

      applyWizardDate(nextDate);
   }

   async function syncSelectionStepDraft(stepKey) {
      const activeConfig = WizardStepConfigs.WIZARD_SELECTION_STEP_DEFINITIONS_BY_KEY[stepKey];
      const activeController = wizardSteps[stepKey];

      if (!WizardStepDraftSync.shouldSyncSelectionStepDraft({
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
      if (WizardStepDraftSync.isWizardDateStep(activeStepKey)) {
         syncDateStepDraft();
         return;
      }

      await syncSelectionStepDraft(activeStepKey);
   }

   async function handleClose() {
      if (WizardStepDraftSync.isWizardDateStep(activeStepKey)) {
         // Only sync the picker when a visit date was already committed
         // (Next/Finish). Syncing the default earliest date into an empty
         // draft would look like an unsaved change on open → close.
         if (wizardState.date) {
            syncDateStepDraft();
         }
      }
      else {
         await syncSelectionStepDraft(activeStepKey);
      }

      if (!wizard.hasUnsavedChanges()) {
         // Clear the overlay only. Remounting the day planner jumps scroll;
         // saved itinerary content is already on the page.
         closeWizard(mountEl);
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
         ...WizardStepConfigs.buildSelectionStepHandlers({
            selectionKey: config.selectionKey,
            preserveOnInvalid: config.preserveOnInvalid,
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
      await finish({ date });
   }

   wizardSteps.date = createDateStepController({
      mountEl,
      earliestSelectableDate: earliestVisitNoon,
      onClose: handleClose,
      onSave: handleDateNext,
      onFinish: handleDateFinish,
   });

   return showStep(WizardStepConfigs.resolveWizardStartStep(startAt));
}
