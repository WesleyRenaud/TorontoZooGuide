import { AnimalDetailViewBuilder } from './animalDetailViewBuilder.js';

export class AnimalDetailView {
   static createAnimalDetailView({ listEl }) {
      function clear() {
         listEl.replaceChildren();
         listEl.scrollTop = 0;
      }

      function render(animalInfo, { exhibitName, onBack }) {
         clear();

         if (!animalInfo) return;

         listEl.appendChild(AnimalDetailViewBuilder.buildBackButton(onBack));
         listEl.appendChild(AnimalDetailViewBuilder.buildAnimalDetailContent(animalInfo, { exhibitName }));
      }

      return { render };
   }
}
