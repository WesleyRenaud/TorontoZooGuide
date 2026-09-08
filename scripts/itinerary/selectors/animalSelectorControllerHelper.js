import { AnimalSelectorModel } from './animalSelector/animalSelectorModel.js';
import { AnimalSelectorRenderer } from './animalSelector/animalSelectorRenderer.js';
import { ConfirmFragment } from '../panel/components/confirmFragment.js';
import { Strings } from '../../strings.js';

export class AnimalSelectorControllerHelper {
   static getAnimalTitle(row) {
      return AnimalSelectorModel.getAnimalTitleLine(row);
   }

   static buildAnimalSearchPayload(query, includeOffDisplayAnimals) {
      return {
         query,
         includeAnimals: true,
         includeOffDisplayAnimals,
         forItinerary: true,
      };
   }

   static shouldConfirmOffDisplayAnimal({
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

   static promptForOffDisplayAnimalSelection(row, proceed) {
      ConfirmFragment.showItineraryConfirmPopup({
         title: Strings.itinerary.confirmation.animalMayBeOffDisplay,
         message: AnimalSelectorModel.buildOffDisplayWarningMessage(row),
         confirmText: Strings.itinerary.actions.add,
         cancelText: Strings.itinerary.actions.cancel,
         onConfirm: proceed,
      });
   }

   static renderOffDisplayAnimalControls({ bodyEl, rerunSearch, onChange }) {
      AnimalSelectorRenderer.renderIncludeOffDisplayToggle({
         bodyEl,
         rerunSearch,
         onChange,
      });
   }
}
