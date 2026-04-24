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
const DEFAULT_ANIMAL_TITLE = 'Animal';
const OFF_DISPLAY_CONFIRM_TITLE = 'Animal May Be Off Display';

function getAnimalTitle(row) {
   return getAnimalSpecies(row) || DEFAULT_ANIMAL_TITLE;
}

function buildAnimalSearchPayload(query, includeOffDisplayAnimals) {
   return {
      query,
      includeAnimals: true,
      includeOffDisplayAnimals,
   };
}

function shouldConfirmOffDisplayAnimal({
   row,
   isSelected,
   includeOffDisplayAnimals,
} = {}) {
   if (isSelected) {
      return false;
   }

   if (!includeOffDisplayAnimals) {
      return false;
   }

   return isLikelyOffDisplayAnimal(row);
}

function promptForOffDisplayAnimalSelection(row, proceed) {
   showItineraryConfirmPopup({
      title: OFF_DISPLAY_CONFIRM_TITLE,
      message: buildOffDisplayWarningMessage(row),
      confirmText: 'Add',
      cancelText: 'Cancel',
      onConfirm: proceed,
   });
}

function renderOffDisplayAnimalControls({ bodyEl, rerunSearch, onChange }) {
   renderIncludeOffDisplayToggle({
      bodyEl,
      rerunSearch,
      onChange,
   });
}

export function createItineraryAnimalSelectorController({ mountEl, onNext, onPrev, onFinish, onClose } = {}) {
   let includeOffDisplayAnimals = false;

   return createItinerarySelectorController({
      mountEl,
      onNext,
      onPrev,
      onFinish,
      onClose,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateStoredAnimals,

      getContext: getItineraryDateSearchContext,

      buildSearchPayload: query => buildAnimalSearchPayload(query, includeOffDisplayAnimals),

      extractRows: response => response.animals,

      getId: getAnimalId,
      getTitle: getAnimalTitle,
      getSubtitle: getAnimalSubtitle,
      getImageSrc: buildAnimalImageSrc,

      makeSelection: makeAnimalSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Add Animals',
      subtitle: 'Search and add animals to your plan.',
      emptyText: 'No animals found.',

      renderRowLeft: renderAnimalSelectorRowLeft,

      onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
         if (!shouldConfirmOffDisplayAnimal({
            row,
            isSelected,
            includeOffDisplayAnimals,
         })) {
            proceed();
            return;
         }

         promptForOffDisplayAnimalSelection(row, proceed);
      },

      renderExtraControls: ({ bodyEl, rerunSearch }) => {
         includeOffDisplayAnimals = false;
         renderOffDisplayAnimalControls({
            bodyEl,
            rerunSearch,
            onChange: (checked) => {
               includeOffDisplayAnimals = checked;
            },
         });
      },
   });
}
