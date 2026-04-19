import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';
import {
   buildAnimalImageSrc,
   buildOffDisplayWarningMessage,
   getAnimalId,
   getAnimalSpecies,
   getAnimalSubtitle,
   isLikelyOffDisplayAnimal,
   makeAnimalSelection,
   migrateStoredAnimals,
} from './animalSelector/model.js';
import {
   renderAnimalSelectorRowLeft,
   renderIncludeOffDisplayToggle,
} from './animalSelector/view.js';

const STORAGE_KEY = 'tzg.itineraryAnimals';

export function createItineraryAnimalSelectorController({ mountEl, onNext, onPrev, onFinish, onClose } = {}) {
   let includeOffDisplayAnimals = false;

   const controller = createItinerarySelectorController({
      mountEl,
      onNext,
      onPrev,
      onFinish,
      onClose,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateStoredAnimals,

      getContext: getItineraryDateSearchContext,

      buildSearchPayload: query => ({
         query,
         includeAnimals: true,
         includeOffDisplayAnimals,
      }),

      extractRows: response => response.animals,

      getId: getAnimalId,
      getTitle: row => getAnimalSpecies(row) || 'Animal',
      getSubtitle: getAnimalSubtitle,
      getImageSrc: buildAnimalImageSrc,

      makeSelection: makeAnimalSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Add Animals',
      subtitle: 'Search and add animals to your plan.',
      emptyText: 'No animals found.',

      renderRowLeft: renderAnimalSelectorRowLeft,

      onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
         if (isSelected) {
            proceed();
            return;
         }

         if (!includeOffDisplayAnimals) {
            proceed();
            return;
         }

         if (!isLikelyOffDisplayAnimal(row)) {
            proceed();
            return;
         }

         showItineraryConfirmPopup({
            title: 'Animal May Be Off Display',
            message: buildOffDisplayWarningMessage(row),
            confirmText: 'Add',
            cancelText: 'Cancel',
            onConfirm: proceed,
         });
      },

      renderExtraControls: ({ bodyEl, rerunSearch }) => {
         includeOffDisplayAnimals = false;
         renderIncludeOffDisplayToggle({
            bodyEl,
            rerunSearch,
            onChange: (checked) => {
               includeOffDisplayAnimals = checked;
            },
         });
      },
   });

   return controller;
}
