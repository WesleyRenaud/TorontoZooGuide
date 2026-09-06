import { AnimalSelectorModel } from './animalSelector/animalSelectorModel.js';
import { View } from './animalSelector/view.js';
import { CreateSelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { ConfirmPopup } from '../panel/components/confirmPopup.js';
import { RegionStorage } from './regionSelector/regionStorage.js';
import { Strings } from '../../strings.js';

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
      title: Strings.itinerary.confirmation.animalMayBeOffDisplay,
      message: AnimalSelectorModel.buildOffDisplayWarningMessage(row),
      confirmText: Strings.itinerary.actions.add,
      cancelText: Strings.itinerary.actions.cancel,
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

export class AnimalSelector {
   static createItineraryAnimalSelectorController({ mountEl, onNext, onPrev, onFinish, onClose } = {}) {
      let includeOffDisplayAnimals = false;

      return CreateSelectorController.createItinerarySelectorController({
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

         topTitle: Strings.itinerary.selectors.builderTitle,
         h1: Strings.itinerary.selectors.titleAnimals,
         subtitle: Strings.itinerary.selectors.animalSubtitle,
         emptyText: Strings.itinerary.emptyText.animals,

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
}
