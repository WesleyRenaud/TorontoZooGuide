import { AnimalDisplayLines } from '../animals/animalDisplayLines.js';
import { AnimalSelectorModel } from '../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { SpeciesOverlayContentBuilder } from './speciesOverlayContentBuilder.js';
import { Strings } from '../strings.js';

export class SpeciesOverlayContent {
   static buildSpeciesContent(animal) {
      const fragment = document.createDocumentFragment();
      const species = SpeciesOverlayContentBuilder.readText(animal?.species);
      const latinName = SpeciesOverlayContentBuilder.readText(animal?.latin_name);
      const titleLine = AnimalDisplayLines.formatSpeciesEnclosureLine(species, AnimalSelectorModel.getAnimalEnclosureName(animal));
      const exhibitLine = AnimalSelectorModel.getAnimalExhibit(animal);

      fragment.appendChild(SpeciesOverlayContentBuilder.createSpeciesImage(animal));
      fragment.appendChild(SpeciesOverlayContentBuilder.createTextElement('h2', 'animal-species-name', titleLine || species));

      if (latinName) {
         fragment.appendChild(SpeciesOverlayContentBuilder.createTextElement('h6', 'latin-name', latinName));
      }

      if (exhibitLine) {
         fragment.appendChild(SpeciesOverlayContentBuilder.createTextElement('h4', 'animal-exhibit', exhibitLine));
      }

      Strings.animalsPage.detailSections.forEach(([title, key]) => {
         SpeciesOverlayContentBuilder.appendIfPresent(
            fragment,
            SpeciesOverlayContentBuilder.createDetailSection(title, animal?.[key])
         );
      });

      return fragment;
   }
}
