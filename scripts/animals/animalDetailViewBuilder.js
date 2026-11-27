import { ValueNormalizer } from '../api/valueNormalizer.js';
import { DetailImageBuilder } from '../assets/detailImageBuilder.js';
import { Strings } from '../strings.js';

export class AnimalDetailViewBuilder {
   static buildBackButton(onBack) {
      const button = document.createElement('button');
      button.className = 'animal-info-back-button';
      button.type = 'button';
      button.textContent = Strings.animalsPage.backWithArrow;
      button.addEventListener('click', () => onBack?.());
      return button;
   }

   static buildDetailSection(title, value) {
      const text = ValueNormalizer.asTrimmedString(value);

      if (!text) {
         return null;
      }

      const section = document.createElement('div');
      section.className = 'section';

      const titleEl = document.createElement('strong');
      titleEl.textContent = Strings.format.labelWithColon(title);

      const bodyEl = document.createElement('p');
      bodyEl.textContent = text;

      section.appendChild(titleEl);
      section.appendChild(bodyEl);

      return section;
   }

   static buildAnimalImage(animal) {
      const species = ValueNormalizer.asTrimmedString(animal.species);
      const src = DetailImageBuilder.buildDetailImageSrcFromParts(
         ['animals', animal.exhibit, species],
         { basePath: `../${DetailImageBuilder.BASE_PATH}` },
      );

      if (!src) {
         return null;
      }

      const image = document.createElement('img');
      image.src = src;
      image.className = 'new-animal-image';
      image.alt = species;

      return image;
   }

   static buildTextElement(tagName, className, text) {
      const value = ValueNormalizer.asTrimmedString(text);

      if (!value) {
         return null;
      }

      const heading = document.createElement(tagName);
      heading.className = className;
      heading.textContent = value;
      return heading;
   }

   static buildViewOnMapButton(animal, exhibitName) {
      const species = ValueNormalizer.asTrimmedString(animal?.species);
      const exhibit = ValueNormalizer.asTrimmedString(exhibitName) || ValueNormalizer.asTrimmedString(animal?.exhibit);

      const button = document.createElement('button');
      button.className = 'view-on-map-button';
      button.type = 'button';
      button.textContent = Strings.common.viewOnMap;

      button.addEventListener('click', () => {
         const url = new URL('map.html', window.location.href);
         url.searchParams.set('focus', species);
         url.searchParams.set('exhibit', exhibit);
         window.location.href = url.toString();
      });

      return button;
   }

   static buildAnimalDetailContent(animal, { exhibitName } = {}) {
      const fragment = document.createDocumentFragment();
      const image = AnimalDetailViewBuilder.buildAnimalImage(animal);
      const speciesNameEl = AnimalDetailViewBuilder.buildTextElement('h2', 'animal-species-name', animal?.species);
      const latinNameEl = AnimalDetailViewBuilder.buildTextElement('p', 'latin-name', animal?.latin_name);
      const exhibitEl = AnimalDetailViewBuilder.buildTextElement('p', 'animal-exhibit', animal?.exhibit);

      if (image) {
         fragment.appendChild(image);
      }

      if (speciesNameEl) {
         fragment.appendChild(speciesNameEl);
      }

      if (latinNameEl) {
         fragment.appendChild(latinNameEl);
      }

      if (exhibitEl) {
         fragment.appendChild(exhibitEl);
         fragment.appendChild(AnimalDetailViewBuilder.buildViewOnMapButton(animal, exhibitName));
      }

      Strings.animalsPage.detailSections.forEach(([title, field]) => {
         const section = AnimalDetailViewBuilder.buildDetailSection(title, animal?.[field]);

         if (section) {
            fragment.appendChild(section);
         }
      });

      return fragment;
   }
}
