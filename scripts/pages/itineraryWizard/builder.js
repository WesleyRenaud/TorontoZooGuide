import { createItineraryDateSelectorController } from '../../itinerary/selectors/dateSelector.js';
import { createItineraryAnimalSelectorController } from '../../itinerary/selectors/animalSelector.js';
import { createItineraryAttractionSelectorController } from '../../itinerary/selectors/attractionSelector.js';
import { createItineraryGuardiansTalkSelectorController } from '../../itinerary/selectors/guardiansTalkSelector.js';
import { createItineraryWildEncounterSelectorController } from '../../itinerary/selectors/wildEncounterSelector.js';

import { showItineraryConfirmPopup } from '../../itinerary/panel/components/confirmPopup.js';
import { showRemovedItemsPopup } from '../../itinerary/panel/components/removedItemsPopup.js';

import { getItinerary } from './itineraryApi.js';
import { loadArray } from '../../itinerary/panel/localStorage.js';
import {
   DATE_KEY,
   ANIMALS_KEY,
   ATTRACTIONS_KEY,
   GUARDIANS_KEY,
   WILD_KEY,
} from './keys.js';
import { finalizeItinerary } from './flow.js';
import { validateItinerary } from './validateItinerary.js';

function getDraftState() {
   return {
      date: localStorage.getItem(DATE_KEY) || '',
      animals: loadArray(ANIMALS_KEY),
      attractions: loadArray(ATTRACTIONS_KEY),
      guardiansTalks: loadArray(GUARDIANS_KEY),
      wildEncounters: loadArray(WILD_KEY),
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

function clearBuilder(mountEl) {
   if (mountEl) {
      mountEl.innerHTML = '';
   }
}

function closeBuilder(mountEl, onDone) {
   clearBuilder(mountEl);
   onDone?.();
}

function applyValidatedSelections(
   validated,
   {
      setAnimals,
      setAttractions,
      setGuardiansTalks,
      setWildEncounters,
   }
) {
   if (!validated) return;

   setAnimals(Array.isArray(validated.animals) ? validated.animals : []);
   setAttractions(Array.isArray(validated.attractions) ? validated.attractions : []);
   setGuardiansTalks(Array.isArray(validated.guardiansTalks) ? validated.guardiansTalks : []);
   setWildEncounters(Array.isArray(validated.wildEncounters) ? validated.wildEncounters : []);
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

function isValidatedItineraryEmpty(validated) {
   if (!validated || typeof validated !== 'object') return true;

   return (
      (!Array.isArray(validated.animals) || validated.animals.length === 0) &&
      (!Array.isArray(validated.attractions) || validated.attractions.length === 0) &&
      (!Array.isArray(validated.guardiansTalks) || validated.guardiansTalks.length === 0) &&
      (!Array.isArray(validated.wildEncounters) || validated.wildEncounters.length === 0)
   );
}

export async function openItineraryBuilder({ mountEl, startAt = 'date', onDone } = {}) {
   if (!mountEl) return;

   const existing = await getItinerary();

   if (existing?.date && !localStorage.getItem(DATE_KEY)) {
      localStorage.setItem(DATE_KEY, existing.date);
   }

   let selectedAnimals = Array.isArray(existing?.animals) ? existing.animals : [];
   let selectedAttractions = Array.isArray(existing?.attractions) ? existing.attractions : [];
   let selectedGuardiansTalks = Array.isArray(existing?.guardiansTalks) ? existing.guardiansTalks : [];
   let selectedWildEncounters = Array.isArray(existing?.wildEncounters) ? existing.wildEncounters : [];

   let pendingRemovedItems = null;
   let pendingValidatedEmpty = false;

   const initialStorageSnapshot = snapshotStorage();
   const initialDraftStateJSON = JSON.stringify(getDraftState());

   function hasUnsavedChanges() {
      return JSON.stringify(getDraftState()) !== initialDraftStateJSON;
   }

   function discardAndClose() {
      restoreStorageSnapshot(initialStorageSnapshot);
      closeBuilder(mountEl, onDone);
   }

   function maybeShowRemovedItemsPopup(removed, isEmptyItinerary = false) {
      if (!hasRemovedItems(removed)) return;

      showRemovedItemsPopup({
         mountEl,
         removed,
         isEmptyItinerary,
         onAccept: () => {},
         onDismiss: () => {},
         onViewAlternatives: (stepKey) => {
            openItineraryBuilder({
               mountEl,
               startAt: stepKey,
               onDone,
            });
         },
      });
   }

   const finish = (override = {}, options = {}) =>
      finalizeItinerary(
         {
            animals: override.animals ?? selectedAnimals,
            attractions: override.attractions ?? selectedAttractions,
            guardiansTalks: override.guardiansTalks ?? selectedGuardiansTalks,
            wildEncounters: override.wildEncounters ?? selectedWildEncounters,
         },
         mountEl,
         {
            allowEmpty: pendingValidatedEmpty || options.allowEmpty === true,
            onDone: () => {
               onDone?.();

               const removedToShow = pendingRemovedItems;
               const wasValidatedEmpty = pendingValidatedEmpty;

               pendingRemovedItems = null;
               pendingValidatedEmpty = false;

               requestAnimationFrame(() => {
                  maybeShowRemovedItemsPopup(removedToShow, wasValidatedEmpty);
               });
            },
         }
      );

   function saveDraftAndClose() {
      const draft = getDraftState();

      selectedAnimals = draft.animals;
      selectedAttractions = draft.attractions;
      selectedGuardiansTalks = draft.guardiansTalks;
      selectedWildEncounters = draft.wildEncounters;

      finalizeItinerary(
         {
            animals: draft.animals,
            attractions: draft.attractions,
            guardiansTalks: draft.guardiansTalks,
            wildEncounters: draft.wildEncounters,
         },
         mountEl,
         { onDone }
      );
   }

   function handleClose() {
      if (!hasUnsavedChanges()) {
         closeBuilder(mountEl, onDone);
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
      onFinish: (wildEncounters) => {
         selectedWildEncounters = Array.isArray(wildEncounters) ? wildEncounters : [];
         finish({ wildEncounters: selectedWildEncounters });
      },
   });

   const guardiansTalkSelector = createItineraryGuardiansTalkSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => attractionSelector.show(),
      onNext: (talks) => {
         selectedGuardiansTalks = Array.isArray(talks) ? talks : [];
         wildEncounterSelector.show();
      },
      onFinish: (talks) => {
         selectedGuardiansTalks = Array.isArray(talks) ? talks : [];
         finish({ guardiansTalks: selectedGuardiansTalks });
      },
   });

   const attractionSelector = createItineraryAttractionSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => animalSelector.show(),
      onNext: (attractions) => {
         selectedAttractions = Array.isArray(attractions) ? attractions : [];
         guardiansTalkSelector.show();
      },
      onFinish: (attractions) => {
         selectedAttractions = Array.isArray(attractions) ? attractions : [];
         finish({ attractions: selectedAttractions });
      },
   });

   const animalSelector = createItineraryAnimalSelectorController({
      mountEl,
      onClose: handleClose,
      onPrev: () => dateSelector.show(),
      onNext: (animals) => {
         selectedAnimals = Array.isArray(animals) ? animals : [];
         attractionSelector.show();
      },
      onFinish: (animals) => {
         selectedAnimals = Array.isArray(animals) ? animals : [];
         finish({ animals: selectedAnimals });
      },
   });

   const dateSelector = createItineraryDateSelectorController({
      mountEl,
      onClose: handleClose,
      onSave: async (date, dateObj) => {
         const result = await validateItinerary({
            date,
            dateObj,
         });

         const validated = result?.validated ?? null;
         const removed = result?.removed ?? null;

         applyValidatedSelections(validated, {
            setAnimals: (value) => {
               selectedAnimals = value;
            },
            setAttractions: (value) => {
               selectedAttractions = value;
            },
            setGuardiansTalks: (value) => {
               selectedGuardiansTalks = value;
            },
            setWildEncounters: (value) => {
               selectedWildEncounters = value;
            },
         });

         pendingRemovedItems = hasRemovedItems(removed) ? removed : null;
         pendingValidatedEmpty = isValidatedItineraryEmpty(validated);

         animalSelector.show();
      },
      onFinish: async (date, dateObj) => {
         const result = await validateItinerary({
            date,
            dateObj,
         });

         const validated = result?.validated ?? null;
         const removed = result?.removed ?? null;

         applyValidatedSelections(validated, {
            setAnimals: (value) => {
               selectedAnimals = value;
            },
            setAttractions: (value) => {
               selectedAttractions = value;
            },
            setGuardiansTalks: (value) => {
               selectedGuardiansTalks = value;
            },
            setWildEncounters: (value) => {
               selectedWildEncounters = value;
            },
         });

         pendingRemovedItems = hasRemovedItems(removed) ? removed : null;
         pendingValidatedEmpty = isValidatedItineraryEmpty(validated);

         finish();
      },
   });

   switch (startAt) {
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