import { normalizeAssetKey } from '../assets/normalizeAssetKey.js';

const SPECIES_DETAIL_SECTIONS = Object.freeze([
   ['Seasonal Viewing Summary', 'seasonal_viewing_summary'],
   ['Seasonal Viewing Information', 'seasonal_viewing_information'],
   ['General Viewing Tips', 'general_viewing_tips'],
   ['Seasonal Viewing Tips', 'seasonal_viewing_tips'],
   ['Identification', 'identification'],
   ['Habitat And Range', 'habitat_and_range'],
   ['Diet And Feeding', 'diet_and_feeding'],
   ['Behaviour And Life Cycle', 'behaviour_and_life_cycle'],
   ['Adaptations', 'adaptations'],
   ['Reproduction And Life Cycle', 'reproduction_and_life_cycle'],
   ['Animals At The Zoo', 'animals_at_the_zoo'],
]);

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
   image.src = `images/details/animals/${normalizeAssetKey(animal.exhibit)}/${normalizeAssetKey(animal.species)}.png`;
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

export function buildSpeciesContent(animal) {
   const fragment = document.createDocumentFragment();
   const species = readText(animal?.species);
   const latinName = readText(animal?.latin_name);
   const exhibit = readText(animal?.exhibit);

   fragment.appendChild(createSpeciesImage(animal));
   fragment.appendChild(createTextElement('h2', 'animal-species-name', species));

   if (latinName) {
      fragment.appendChild(createTextElement('h6', 'latin-name', latinName));
   }

   fragment.appendChild(createTextElement('h4', 'animal-exhibit', exhibit));

   SPECIES_DETAIL_SECTIONS.forEach(([title, key]) => {
      appendIfPresent(
         fragment,
         createDetailSection(title, animal?.[key])
      );
   });

   return fragment;
}
