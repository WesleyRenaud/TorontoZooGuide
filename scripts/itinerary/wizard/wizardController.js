import { DraftStore } from '../draftStore.js';
import { FilterDraftExcludingWarningFixedTimeItems } from './filterDraftExcludingWarningFixedTimeItems.js';
import { ConfirmFragment } from '../../itinerary/panel/components/confirmFragment.js';
import { DateSelector } from '../../itinerary/selectors/dateSelector.js';
import { ItineraryConfirmationResult } from '../itineraryConfirmationResult.js';
import { ItineraryService } from '../itineraryService.js';
import { ItineraryShape } from '../itineraryShape.js';
import { ItineraryWizardStore } from './itineraryWizardStore.js';
import { SectionConfigs } from '../panel/sectionConfigs.js';
import { Strings } from '../../strings.js';
import { VisitDateResolver } from '../visitDateResolver.js';
import { WizardControllerHelper } from './wizardControllerHelper.js';
import { WizardDraft } from './wizardDraft.js';
import { WizardFinalizePresenter } from './wizardFinalizePresenter.js';
import { WizardFinalizer } from './wizardFinalizer.js';
import { WizardStepConfigs } from './wizardStepConfigs.js';
import { WizardStepDraftSynchronizer } from './wizardStepDraftSynchronizer.js';

export class WizardController {
   static async openItineraryWizard({
   mountEl,
   startAt = WizardStepConfigs.WIZARD_DEFAULT_START_STEP,
   deps = {},
} = {}) {
      const {
         loadItinerary = ItineraryService.getItinerary,
         resolveEarliestVisitDate = VisitDateResolver.resolveEarliestSelectableVisitDateNoon,
         createWizardState = ItineraryWizardStore.createItineraryWizardState,
         createDateStepController = DateSelector.createItineraryDateSelectorController,
         finalizeWizard = WizardFinalizer.finalizeItineraryWizard,
         showConfirmPopup = ConfirmFragment.showItineraryConfirmPopup,
         syncAnimalDraft = DraftStore.syncItineraryAnimalDraftFromItinerary,
         loadSelectionStepConfigs = WizardControllerHelper.loadDefaultSelectionStepConfigs,
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
      else if (!existing || ItineraryService.isItineraryEmpty(existing)) {
         DraftStore.clearItinerarySelectionStorage();
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
            && !WizardFinalizePresenter.shouldBlockEmptyFinish(
               WizardDraft.buildWizardDraft(wizardState),
               wizard.allowEmptyFinish(options.allowEmpty)
            )
         ) {
            // Clear the overlay only. Do not remount the day planner — that jumps
            // scroll. Saved itinerary content is already on the page.
            WizardControllerHelper.clearWizard(mountEl);
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
         WizardControllerHelper.closeWizard(mountEl);
      }

      function applyWizardDate(date) {
         wizard.applyValidationResult(date, null);
      }

      function syncDateStepDraft() {
         const nextDate = WizardStepDraftSynchronizer.resolveDateStepDraftUpdate({
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

         if (!WizardStepDraftSynchronizer.shouldSyncSelectionStepDraft({
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
         if (WizardStepDraftSynchronizer.isWizardDateStep(activeStepKey)) {
            syncDateStepDraft();
            return;
         }

         await syncSelectionStepDraft(activeStepKey);
      }

      async function handleClose() {
         if (WizardStepDraftSynchronizer.isWizardDateStep(activeStepKey)) {
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
            WizardControllerHelper.closeWizard(mountEl);
            return;
         }

         showConfirmPopup({
            title: Strings.itinerary.confirmation.saveChangesTitle,
            message: Strings.itinerary.confirmation.saveChangesMessage,
            confirmText: Strings.actions.save,
            cancelText: Strings.itinerary.actions.discard,
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
}
