import { createItineraryDateSelectorController } from '../../itinerary/selectors/dateSelector.js';
import { createItineraryRegionSelectorController } from '../../itinerary/selectors/regionSelector.js';
import { createItineraryAnimalSelectorController } from '../../itinerary/selectors/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../../itinerary/selectors/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../../itinerary/selectors/guardiansTalkSelector.js';
import { createItineraryWildEncounterSelectorController } from '../../itinerary/selectors/wildEncounterSelector.js';

import { showItineraryConfirmPopup } from '../../itinerary/panel/components/confirmPopup.js';
import { showRemovedItemsPopup } from '../../itinerary/panel/components/removedItemsPopup.js';

import { getItinerary } from '../itineraryService.js';
import { loadArray } from '../panel/localStorage.js';
import {
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
} from '../storageKeys.js';
import { finalizeItineraryWizard } from './wizardFinalizer.js';
import { validateItineraryDraft } from './draftValidator.js';

function getDraftState() {
   return {
      date: localStorage.getItem(DATE_KEY) || '',
      animals: loadArray(ANIMALS_KEY),
      attractions: loadArray(ATTRACTIONS_KEY),
      guardiansTalks: loadArray(GUARDIANS_KEY),
      wildEncounters: loadArray(WILD_KEY),
   };
}

function writeDraftState({
   date = '',
   animals = [],
   attractions = [],
   guardiansTalks = [],
   wildEncounters = [],
}) {
   if (date) {
      localStorage.setItem(DATE_KEY, date);
   } else {
      localStorage.removeItem(DATE_KEY);
   }

   localStorage.setItem(
      ANIMALS_KEY,
      JSON.stringify(Array.isArray(animals) ? animals : [])
   );

   localStorage.setItem(
      ATTRACTIONS_KEY,
      JSON.stringify(Array.isArray(attractions) ? attractions : [])
   );

   localStorage.setItem(
      GUARDIANS_KEY,
      JSON.stringify(Array.isArray(guardiansTalks) ? guardiansTalks : [])
   );

   localStorage.setItem(
      WILD_KEY,
      JSON.stringify(Array.isArray(wildEncounters) ? wildEncounters : [])
   );
}

function getWizardSelections(wizardState) {
   return {
      date: wizardState.date,
      animals: wizardState.animals,
      attractions: wizardState.attractions,
      guardiansTalks: wizardState.guardiansTalks,
      wildEncounters: wizardState.wildEncounters,
   };
}

function snapshotStorage() {
   return {
      [DATE_KEY]: localStorage.getItem(DATE_KEY),
      [ANIMALS_KEY]: localStorage.getItem(ANIMALS_KEY),
      [ATTRACTIONS_KEY]: localStorage.getItem(ATTRACTIONS_KEY),
      [GUARDIANS_KEY]: localStorage.getItem(GUARDIANS_KEY),
      [WILD_KEY]: localStorage.getItem(WILD_KEY),
   };
}

function restoreStorageSnapshot(snapshot) {
   Object.entries(snapshot).forEach(([key, value]) => {
      if (value == null) {
         localStorage.removeItem(key);
      } else {
         localStorage.setItem(key, value);
      }
   });
}

function clearWizard(mountEl) {
   if (mountEl) {
      mountEl.innerHTML = '';
   }
}

function closeWizard(mountEl, onDone) {
   clearWizard(mountEl);
   onDone?.();
}

function applyValidatedSelections(validated, wizardState) {
   if (!validated) return;

   wizardState.animals = Array.isArray(validated.animals) ? validated.animals : [];
   wizardState.attractions = Array.isArray(validated.attractions) ? validated.attractions : [];
   wizardState.guardiansTalks = Array.isArray(validated.guardiansTalks) ? validated.guardiansTalks : [];
   wizardState.wildEncounters = Array.isArray(validated.wildEncounters) ? validated.wildEncounters : [];
}

function hasRemovedItems(removed) {
   if (!removed || typeof removed !== 'object') return false;

   return (
      (Array.isArray(removed.animals) && removed.animals.length > 0) ||
      (Array.isArray(removed.attractions) && removed.attractions.length > 0) ||
      (Array.isArray(removed.guardiansTalks) && removed.guardiansTalks.length > 0) ||
      (Array.isArray(removed.wildEncounters) && removed.wildEncounters.length > 0)
   );
}

function hasReducedVisibility(reducedVisibility) {
   if (!reducedVisibility || typeof reducedVisibility !== 'object') return false;

   return (
      Array.isArray(reducedVisibility.animals) &&
      reducedVisibility.animals.length > 0
   );
}

function hasImprovedVisibility(improvedVisibility) {
   if (!improvedVisibility || typeof improvedVisibility !== 'object') return false;

   return (
      Array.isArray(improvedVisibility.animals) &&
      improvedVisibility.animals.length > 0
   );
}

function isValidatedItineraryEmpty(validated) {
   if (!validated || typeof validated !== 'object') return true;

   return (
      (!Array.isArray(validated.animals) || validated.animals.length === 0) &&
      (!Array.isArray(validated.attractions) || validated.attractions.length === 0) &&
      (!Array.isArray(validated.guardiansTalks) || validated.guardiansTalks.length === 0) &&
      (!Array.isArray(validated.wildEncounters) || validated.wildEncounters.length === 0)
   );
}

export async function openItineraryWizard({ mountEl, startAt = 'date', onDone } = {}) {
   if (!mountEl) return;

   const existing = await getItinerary();

   const existingDate = existing?.date || '';
   const existingAnimals = Array.isArray(existing?.animals) ? existing.animals : [];
   const existingAttractions = Array.isArray(existing?.attractions) ? existing.attractions : [];
   const existingGuardiansTalks = Array.isArray(existing?.guardiansTalks) ? existing.guardiansTalks : [];
   const existingWildEncounters = Array.isArray(existing?.wildEncounters) ? existing.wildEncounters : [];

   const wizardState = {
      date: existingDate,
      animals: existingAnimals,
      attractions: existingAttractions,
      guardiansTalks: existingGuardiansTalks,
      wildEncounters: existingWildEncounters,
      pendingRemovedItems: null,
      pendingReducedVisibility: null,
      pendingImprovedVisibility: null,
      pendingValidatedEmpty: false,
   };

   writeDraftState(getWizardSelections(wizardState));

   const initialStorageSnapshot = snapshotStorage();
   const initialDraftStateJSON = JSON.stringify(getDraftState());

   function hasUnsavedChanges() {
      return JSON.stringify(getDraftState()) !== initialDraftStateJSON;
   }

   function discardAndClose() {
      restoreStorageSnapshot(initialStorageSnapshot);
      closeWizard(mountEl, onDone);
   }

   function persistDraft() {
      writeDraftState(getWizardSelections(wizardState));
   }

   function updateSelection(key, value, { preserveOnInvalid = false } = {}) {
      wizardState[key] = Array.isArray(value)
         ? value
         : preserveOnInvalid
            ? wizardState[key]
            : [];

      persistDraft();
   }

   function applyValidationResult(date, result) {
      const validated = result?.validated ?? null;
      const removed = result?.removed ?? null;
      const reducedVisibility = result?.reducedVisibility ?? null;
      const improvedVisibility = result?.improvedVisibility ?? null;

      applyValidatedSelections(validated, wizardState);

      wizardState.date = date;
      wizardState.pendingRemovedItems = hasRemovedItems(removed) ? removed : null;
      wizardState.pendingReducedVisibility = hasReducedVisibility(reducedVisibility) ? reducedVisibility : null;
      wizardState.pendingImprovedVisibility = hasImprovedVisibility(improvedVisibility) ? improvedVisibility : null;
      wizardState.pendingValidatedEmpty = isValidatedItineraryEmpty(validated);

      persistDraft();
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

   function maybeShowRemovedItemsPopup(
      removed,
      reducedVisibility,
      improvedVisibility,
      isEmptyItinerary = false
   ) {
      if (
         !hasRemovedItems(removed) &&
         !hasReducedVisibility(reducedVisibility) &&
         !hasImprovedVisibility(improvedVisibility)
      ) {
         return;
      }

      showRemovedItemsPopup({
         mountEl,
         removed,
         reducedVisibility,
         improvedVisibility,
         isEmptyItinerary,
         onAccept: () => {},
         onDismiss: () => {},
         onViewAlternatives: (stepKey) => {
            openItineraryWizard({
               mountEl,
               startAt: stepKey,
               onDone,
            });
         },
      });
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
            allowEmpty: wizardState.pendingValidatedEmpty || options.allowEmpty === true,
            onDone: () => {
               onDone?.();

               const removedToShow = wizardState.pendingRemovedItems;
               const reducedVisibilityToShow = wizardState.pendingReducedVisibility;
               const improvedVisibilityToShow = wizardState.pendingImprovedVisibility;
               const wasValidatedEmpty = wizardState.pendingValidatedEmpty;

               wizardState.pendingRemovedItems = null;
               wizardState.pendingReducedVisibility = null;
               wizardState.pendingImprovedVisibility = null;
               wizardState.pendingValidatedEmpty = false;

               requestAnimationFrame(() => {
                  maybeShowRemovedItemsPopup(
                     removedToShow,
                     reducedVisibilityToShow,
                     improvedVisibilityToShow,
                     wasValidatedEmpty
                  );
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
      if (!hasUnsavedChanges()) {
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

   async function getAllSelectableAnimals() {
      // Replace this whole function with the shared animal-selector fetch helper.
      // For example:
      // return await getSelectableAnimalsForCurrentItineraryDate();

      return wizardState.animals;
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
      getAllSelectableAnimals,
   });

   async function handleDateSelection(date, dateObj) {
      const result = await validateItineraryDraft({
         date,
         dateObj,
      });

      applyValidationResult(date, result);
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
