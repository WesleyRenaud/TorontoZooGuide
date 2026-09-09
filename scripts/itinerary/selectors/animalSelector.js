import { AnimalSelectorModel } from './animalSelector/animalSelectorModel.js';
import { AnimalSelectorRenderer } from './animalSelector/animalSelectorRenderer.js';
import { AnimalSelectorControllerHelper } from './animalSelectorControllerHelper.js';
import { ItinerarySearchContext } from '../itinerarySearchContext.js';
import { RegionStorageStore } from './regionSelector/regionStorageStore.js';
import { SelectorControllerFactory } from './selectorControllerFactory.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { StorageKeys } from '../storageKeys.js';
import { Strings } from '../../strings.js';

export class AnimalSelector {
   static STORAGE_KEY = StorageKeys.ANIMALS_KEY;

   static createItineraryAnimalSelectorController({ mountEl, onNext, onPrev, onFinish, onClose } = {}) {
      let includeOffDisplayAnimals = false;

      return SelectorControllerFactory.createItinerarySelectorController({
         mountEl,
         onNext,
         onPrev,
         onFinish,
         onClose,

         storageKey: AnimalSelector.STORAGE_KEY,
         migrateSelected: AnimalSelectorModel.migrateStoredAnimals,

         getContext: ItinerarySearchContext.getItineraryDateSearchContext,

         buildSearchPayload: query => AnimalSelectorControllerHelper.buildAnimalSearchPayload(query, includeOffDisplayAnimals),

         extractRows: response => response[ScheduleItemKind.ANIMAL.itemType],

         getId: AnimalSelectorModel.getAnimalId,
         getTitle: AnimalSelectorControllerHelper.getAnimalTitle,
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
                  RegionStorageStore.restoreRemovedAnimalKey(AnimalSelectorModel.getAnimalId(row));
               }

               proceed();
            };

            if (!AnimalSelectorControllerHelper.shouldConfirmOffDisplayAnimal({
               row,
               isSelected,
               includeOffDisplayAnimals,
            })) {
               completeToggle();
               return;
            }

            AnimalSelectorControllerHelper.promptForOffDisplayAnimalSelection(row, completeToggle);
         },

         renderExtraControls: ({ bodyEl, rerunSearch }) => {
            includeOffDisplayAnimals = false;
            AnimalSelectorControllerHelper.renderOffDisplayAnimalControls({
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
