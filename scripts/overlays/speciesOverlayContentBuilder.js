import { ValueNormalizer } from '../api/valueNormalizer.js';
import { AssetKeyNormalizer } from '../assets/assetKeyNormalizer.js';

export class SpeciesOverlayContentBuilder {
   static createTextElement(tagName, className, text) {
      const element = document.createElement(tagName);
      element.className = className;
      element.textContent = text;
      return element;
   }

   static createSpeciesImage(animal) {
      const image = document.createElement('img');
      image.className = 'new-animal-image';
      image.src = `images/details/animals/${AssetKeyNormalizer.normalize(animal.exhibit)}/${AssetKeyNormalizer.normalize(animal.species)}.png`;
      image.alt = ValueNormalizer.asTrimmedString(animal.species);
      return image;
   }

   static createDetailSection(title, value) {
      const text = ValueNormalizer.asTrimmedString(value);

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

   static appendIfPresent(parent, child) {
      if (child) {
         parent.appendChild(child);
      }
   }
}
