import { AnimalDisplayLines } from '../animals/animalDisplayLines.js';
import { AssetKeyNormalizer } from '../assets/assetKeyNormalizer.js';
import { AnimalSelectorModel } from '../itinerary/selectors/animalSelector/animalSelectorModel.js';
import { APP_STRINGS } from '../strings.js';

function readText(value) {
   return typeof value === 'string'
      ? value.trim()
      : '';
}

function createTextElement(tagName, className, text) {
   const element = document.createElement(tagName);
   element.className = className;
   element.textContent = text;
   return element;
}

function createSpeciesImage(animal) {
   const image = document.createElement('img');
   image.className = 'new-animal-image';
   image.src = `images/details/animals/${AssetKeyNormalizer.normalize(animal.exhibit)}/${AssetKeyNormalizer.normalize(animal.species)}.png`;
   image.alt = readText(animal.species);
   return image;
}

function createDetailSection(title, value) {
   const text = readText(value);

   if (!text) {
      return null;
   }

   const section = document.createElement('div');
   section.className = 'section';

   const heading = document.createElement('strong');
   heading.textContent = `${title}:`;

   const paragraph = document.createElement('p');
   paragraph.textContent = text;

   section.append(heading, paragraph);

   return section;
}

function appendIfPresent(parent, child) {
   if (child) {
      parent.appendChild(child);
   }
}

export class SpeciesOverlayContent {
   static buildSpeciesContent(animal) {
      const fragment = document.createDocumentFragment();
      const species = readText(animal?.species);
      const latinName = readText(animal?.latin_name);
      const titleLine = AnimalDisplayLines.formatSpeciesEnclosureLine(species, AnimalSelectorModel.getAnimalEnclosureName(animal));
      const exhibitLine = AnimalSelectorModel.getAnimalExhibit(animal);

      fragment.appendChild(createSpeciesImage(animal));
      fragment.appendChild(createTextElement('h2', 'animal-species-name', titleLine || species));

      if (latinName) {
         fragment.appendChild(createTextElement('h6', 'latin-name', latinName));
      }

      if (exhibitLine) {
         fragment.appendChild(createTextElement('h4', 'animal-exhibit', exhibitLine));
      }

      APP_STRINGS.animalsPage.detailSections.forEach(([title, key]) => {
         appendIfPresent(
            fragment,
            createDetailSection(title, animal?.[key])
         );
      });

      return fragment;
   }
}
