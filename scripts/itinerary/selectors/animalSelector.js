import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';
import { APP_STRINGS } from '../../strings.js';
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
function getAnimalTitle(row) {
   return getAnimalSpecies(row) || APP_STRINGS.entityLabels.animal;
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
      title: APP_STRINGS.itinerary.confirmation.animalMayBeOffDisplay,
      message: buildOffDisplayWarningMessage(row),
      confirmText: APP_STRINGS.itinerary.actions.add,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
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

      topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
      h1: APP_STRINGS.itinerary.selectors.titleAnimals,
      subtitle: APP_STRINGS.itinerary.selectors.animalSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.animals,

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
