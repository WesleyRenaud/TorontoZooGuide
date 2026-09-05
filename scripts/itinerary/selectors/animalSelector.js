import { AnimalSelectorModel } from './animalSelector/animalSelectorModel.js';
import { View } from './animalSelector/view.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { RegionStorage } from './regionSelector/regionStorage.js';
import { APP_STRINGS } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryAnimals';
function getAnimalTitle(row) {
   return AnimalSelectorModel.getAnimalTitleLine(row);
}

function buildAnimalSearchPayload(query, includeOffDisplayAnimals) {
   return {
      query,
      includeAnimals: true,
      includeOffDisplayAnimals,
      forItinerary: true,
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

   return AnimalSelectorModel.isLikelyOffDisplayAnimal(row);
}

function promptForOffDisplayAnimalSelection(row, proceed) {
   ConfirmPopup.showItineraryConfirmPopup({
      title: APP_STRINGS.itinerary.confirmation.animalMayBeOffDisplay,
      message: AnimalSelectorModel.buildOffDisplayWarningMessage(row),
      confirmText: APP_STRINGS.itinerary.actions.add,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      onConfirm: proceed,
   });
}

function renderOffDisplayAnimalControls({ bodyEl, rerunSearch, onChange }) {
   View.renderIncludeOffDisplayToggle({
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
      migrateSelected: AnimalSelectorModel.migrateStoredAnimals,

      getContext: ItinerarySearchContext.getItineraryDateSearchContext,

      buildSearchPayload: query => buildAnimalSearchPayload(query, includeOffDisplayAnimals),

      extractRows: response => response.animals,

      getId: AnimalSelectorModel.getAnimalId,
      getTitle: getAnimalTitle,
      getSubtitle: AnimalSelectorModel.getAnimalSubtitle,
      getImageSrc: AnimalSelectorModel.buildAnimalImageSrc,

      makeSelection: AnimalSelectorModel.makeAnimalSelection,

      topTitle: APP_STRINGS.itinerary.selectors.builderTitle,
      h1: APP_STRINGS.itinerary.selectors.titleAnimals,
      subtitle: APP_STRINGS.itinerary.selectors.animalSubtitle,
      emptyText: APP_STRINGS.itinerary.emptyText.animals,

      renderRowLeft: View.renderAnimalSelectorRowLeft,

      onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
         const completeToggle = () => {
            if (!isSelected) {
               RegionStorage.restoreRemovedAnimalKey(AnimalSelectorModel.getAnimalId(row));
            }

            proceed();
         };

         if (!shouldConfirmOffDisplayAnimal({
            row,
            isSelected,
            includeOffDisplayAnimals,
         })) {
            completeToggle();
            return;
         }

         promptForOffDisplayAnimalSelection(row, completeToggle);
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
