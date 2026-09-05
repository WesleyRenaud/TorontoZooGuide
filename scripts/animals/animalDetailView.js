import { AssetKeyNormalizer } from '../assets/assetKeyNormalizer.js';
import { APP_STRINGS } from '../strings.js';

function readText(value = '') {
   return typeof value === 'string'
      ? value.trim()
      : '';
}

function buildBackButton(onBack) {
   const button = document.createElement('button');
   button.className = 'animal-info-back-button';
   button.type = 'button';
   button.textContent = APP_STRINGS.animalsPage.backWithArrow;
   button.addEventListener('click', () => onBack?.());
   return button;
}

function buildDetailSection(title, value) {
   const text = readText(value);

   if (!text) {
      return null;
   }

   const section = document.createElement('div');
   section.className = 'section';

   const titleEl = document.createElement('strong');
   titleEl.textContent = `${title}:`;

   const bodyEl = document.createElement('p');
   bodyEl.textContent = text;

   section.appendChild(titleEl);
   section.appendChild(bodyEl);

   return section;
}

function buildAnimalImage(animal) {
   const exhibitFile = AssetKeyNormalizer.normalize(readText(animal?.exhibit));
   const species = readText(animal?.species);
   const speciesFile = AssetKeyNormalizer.normalize(species);

   if (!exhibitFile || !speciesFile) {
      return null;
   }

   const image = document.createElement('img');
   image.src = `../images/details/animals/${exhibitFile}/${speciesFile}.png`;
   image.className = 'new-animal-image';
   image.alt = species;

   return image;
}

function buildHeading(tagName, className, text) {
   const value = readText(text);

   if (!value) {
      return null;
   }

   const heading = document.createElement(tagName);
   heading.className = className;
   heading.textContent = value;
   return heading;
}

function buildViewOnMapButton(animal, exhibitName) {
   const species = readText(animal?.species);
   const exhibit = readText(exhibitName) || readText(animal?.exhibit);

   const button = document.createElement('button');
   button.className = 'view-on-map-button';
   button.type = 'button';
   button.textContent = APP_STRINGS.common.viewOnMap;

   button.addEventListener('click', () => {
      const url = new URL('map.html', window.location.href);
      url.searchParams.set('focus', species);
      url.searchParams.set('exhibit', exhibit);
      window.location.href = url.toString();
   });

   return button;
}

function buildAnimalDetailContent(animal, { exhibitName } = {}) {
   const fragment = document.createDocumentFragment();
   const image = buildAnimalImage(animal);
   const speciesHeading = buildHeading('h2', 'animal-species-name', animal?.species);
   const latinHeading = buildHeading('h6', 'latin-name', animal?.latin_name);
   const exhibitHeading = buildHeading('h4', 'animal-exhibit', animal?.exhibit);

   if (image) {
      fragment.appendChild(image);
   }

   if (speciesHeading) {
      fragment.appendChild(speciesHeading);
   }

   if (latinHeading) {
      fragment.appendChild(latinHeading);
   }

   if (exhibitHeading) {
      fragment.appendChild(exhibitHeading);
      fragment.appendChild(buildViewOnMapButton(animal, exhibitName));
   }

   APP_STRINGS.animalsPage.detailSections.forEach(([title, field]) => {
      const section = buildDetailSection(title, animal?.[field]);

      if (section) {
         fragment.appendChild(section);
      }
   });

   return fragment;
}

export class AnimalDetailView {
   static createAnimalDetailView({ listEl }) {
      function clear() {
         listEl.replaceChildren();
         listEl.scrollTop = 0;
      }

      function render(animalInfo, { exhibitName, onBack }) {
         clear();

         if (!animalInfo) return;

         listEl.appendChild(buildBackButton(onBack));
         listEl.appendChild(buildAnimalDetailContent(animalInfo, { exhibitName }));
      }

      return { render };
   }
}
