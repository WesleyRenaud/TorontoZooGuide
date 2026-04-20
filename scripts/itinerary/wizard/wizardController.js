import { createItineraryDateSelectorController } from '../../itinerary/selectors/dateSelector.js';
import { createItineraryRegionSelectorController } from '../../itinerary/selectors/regionSelector.js';
import { createItineraryAnimalSelectorController } from '../../itinerary/selectors/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../../itinerary/selectors/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../../itinerary/selectors/guardiansTalkSelector.js';
import { createItineraryWildEncounterSelectorController } from '../../itinerary/selectors/wildEncounterSelector.js';

import { showItineraryConfirmPopup } from '../../itinerary/panel/components/confirmPopup.js';

import { getItinerary } from '../itineraryService.js';
import { finalizeItineraryWizard } from './wizardFinalizer.js';
import { validateItineraryDraft } from './draftValidator.js';
import { createItineraryWizardState } from './state.js';
import { showWizardValidationPopupIfNeeded } from './validationPopup.js';

function clearWizard(mountEl) {
   if (mountEl) {
      mountEl.innerHTML = '';
   }
}

function closeWizard(mountEl, onDone) {
   clearWizard(mountEl);
   onDone?.();
}

export async function openItineraryWizard({ mountEl, startAt = 'date', onDone } = {}) {
   if (!mountEl) return;

   const existing = await getItinerary();
   const wizard = createItineraryWizardState(existing ?? {});
   const { state: wizardState } = wizard;

   function discardAndClose() {
      wizard.discardChanges();
      closeWizard(mountEl, onDone);
   }

   function updateSelection(key, value, { preserveOnInvalid = false } = {}) {
      wizard.updateSelection(key, value, { preserveOnInvalid });
   }

   function createSelectionStepHandlers({
      key,
      next,
      preserveOnInvalid = false,
   } = {}) {
      return {
         onNext: next
            ? value => {
               updateSelection(key, value, { preserveOnInvalid });
               next();
            }
            : undefined,
         onFinish: value => {
               updateSelection(key, value, { preserveOnInvalid });
               finish({ [key]: wizardState[key] });
         },
      };
   }

   const finish = (override = {}, options = {}) =>
      finalizeItineraryWizard(
         {
            animals: override.animals ?? wizardState.animals,
            attractions: override.attractions ?? wizardState.attractions,
            guardiansTalks: override.guardiansTalks ?? wizardState.guardiansTalks,
            wildEncounters: override.wildEncounters ?? wizardState.wildEncounters,
         },
         mountEl,
         {
            allowEmpty: wizard.allowEmptyFinish(options.allowEmpty),
            onDone: () => {
               onDone?.();
               const pendingValidation = wizard.consumePendingValidation();

               requestAnimationFrame(() => {
                  showWizardValidationPopupIfNeeded({
                     mountEl,
                     pendingValidation,
                     onViewAlternatives: (stepKey) => {
                        openItineraryWizard({
                           mountEl,
                           startAt: stepKey,
                           onDone,
                        });
                     },
                  });
               });
            },
         }
      );

   function saveDraftAndClose() {
      finalizeItineraryWizard(
         {
            animals: wizardState.animals,
            attractions: wizardState.attractions,
            guardiansTalks: wizardState.guardiansTalks,
            wildEncounters: wizardState.wildEncounters,
         },
         mountEl,
         { onDone }
      );
   }

   function handleClose() {
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
            saveDraftAndClose();
         },
         onCancel: () => {
            discardAndClose();
         },
         });
   }

   const wildEncounterSelector = createItineraryWildEncounterSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => guardiansTalkSelector.show(),
      onFinish: createSelectionStepHandlers({
         key: 'wildEncounters',
      }).onFinish,
   });

   const guardiansTalkSelector = createItineraryGuardiansTalkSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => attractionSelector.show(),
      ...createSelectionStepHandlers({
         key: 'guardiansTalks',
         next: () => wildEncounterSelector.show(),
      }),
   });

   const attractionSelector = createItineraryAttractionSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => animalSelector.show(),
      ...createSelectionStepHandlers({
         key: 'attractions',
         next: () => guardiansTalkSelector.show(),
      }),
   });

   const animalSelector = createItineraryAnimalSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => regionSelector.show(),
      ...createSelectionStepHandlers({
         key: 'animals',
         next: () => attractionSelector.show(),
      }),
   });

   const regionSelector = createItineraryRegionSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => dateSelector.show(),
      ...createSelectionStepHandlers({
         key: 'animals',
         next: () => animalSelector.show(),
         preserveOnInvalid: true,
      }),
   });

   async function handleDateSelection(date, dateObj) {
      const result = await validateItineraryDraft({
         date,
         dateObj,
      });

      wizard.applyValidationResult(date, result);
      regionSelector.show();
   }

   const dateSelector = createItineraryDateSelectorController({
      mountEl,
      onClose: handleClose,
      onSave: handleDateSelection,
      onFinish: handleDateSelection,
   });

   switch (startAt) {
      case 'regions':
         return regionSelector.show();
      case 'animals':
         return animalSelector.show();
      case 'attractions':
         return attractionSelector.show();
      case 'guardiansTalks':
         return guardiansTalkSelector.show();
      case 'wildEncounters':
         return wildEncounterSelector.show();
      case 'date':
      default:
         return dateSelector.show();
   }
}
