import { AnimalSelectorModel } from './animalSelector/animalSelectorModel.js';
import { AnimalSelectorRenderer } from './animalSelector/animalSelectorRenderer.js';
import { AnimalSelectorControllerHelpers } from './animalSelectorControllerHelpers.js';
import { CreateSelectorController } from './createSelectorController.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { RegionStorage } from './regionSelector/regionStorage.js';
import { Strings } from '../../strings.js';

const STORAGE_KEY = 'tzg.itineraryAnimals';

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

         buildSearchPayload: query => AnimalSelectorControllerHelpers.buildAnimalSearchPayload(query, includeOffDisplayAnimals),

         extractRows: response => response.animals,

         getId: AnimalSelectorModel.getAnimalId,
         getTitle: AnimalSelectorControllerHelpers.getAnimalTitle,
         getSubtitle: AnimalSelectorModel.getAnimalSubtitle,
         getImageSrc: AnimalSelectorModel.buildAnimalImageSrc,

         makeSelection: AnimalSelectorModel.makeAnimalSelection,

         topTitle: Strings.itinerary.selectors.builderTitle,
         h1: Strings.itinerary.selectors.titleAnimals,
         subtitle: Strings.itinerary.selectors.animalSubtitle,
         emptyText: Strings.itinerary.emptyText.animals,

         renderRowLeft: AnimalSelectorRenderer.renderAnimalSelectorRowLeft,

         onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
            const completeToggle = () => {
               if (!isSelected) {
                  RegionStorage.restoreRemovedAnimalKey(AnimalSelectorModel.getAnimalId(row));
               }

               proceed();
            };

            if (!AnimalSelectorControllerHelpers.shouldConfirmOffDisplayAnimal({
               row,
               isSelected,
               includeOffDisplayAnimals,
            })) {
               completeToggle();
               return;
            }

            AnimalSelectorControllerHelpers.promptForOffDisplayAnimalSelection(row, completeToggle);
         },

         renderExtraControls: ({ bodyEl, rerunSearch }) => {
            includeOffDisplayAnimals = false;
            AnimalSelectorControllerHelpers.renderOffDisplayAnimalControls({
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
