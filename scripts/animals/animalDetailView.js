import { normalizeParameter } from '../utils/normalize.js';

export function createAnimalDetailView({ listEl }) {
   function clear() {
      listEl.innerHTML = '';
      listEl.scrollTop = 0;
   }

   function buildBackButtonHTML() {
      return `
         <button class="animal-info-back-button" type="button">
            ← Back
         </button>
      `;
   }

   function buildSpeciesContentHTML(animal) {
      const section = (title, value) => {
         if (!value || !String(value).trim()) return '';
         return `
            <div class="section">
               <strong>${title}:</strong>
               <p>${value}</p>
            </div>
         `;
      };

      const exhibitFile = normalizeParameter(animal.exhibit || '');
      const speciesFile = normalizeParameter(animal.species || '');

      return `
         <img
            src="../images/animals/${exhibitFile}/${speciesFile}.png"
            class="new-animal-image"
         >

         <h2 class="animal-species-name">${animal.species || ''}</h2>
         ${animal.latin_name ? `<h6 class="latin-name">${animal.latin_name}</h6>` : ''}
         <h4 class="animal-exhibit">${animal.exhibit || ''}</h4>

         ${section('Seasonal Viewing Summary', animal.seasonal_viewing_summary)}
         ${section('Seasonal Viewing Information', animal.seasonal_viewing_information)}
         ${section('General Viewing Tips', animal.general_viewing_tips)}
         ${section('Seasonal Viewing Tips', animal.seasonal_viewing_tips)}
         ${section('Identification', animal.identification)}
         ${section('Habitat And Range', animal.habitat_and_range)}
         ${section('Diet And Feeding', animal.diet_and_feeding)}
         ${section('Behaviour And Life Cycle', animal.behaviour_and_life_cycle)}
         ${section('Adaptations', animal.adaptations)}
         ${section('Reproduction And Life Cycle', animal.reproduction_and_life_cycle)}
         ${section('Animals At The Zoo', animal.animals_at_the_zoo)}
      `;
   }

   function render(animalInfo, { regionName, exhibitName, onBack }) {
      clear();

      if (!animalInfo) return;

      listEl.innerHTML = buildBackButtonHTML() + buildSpeciesContentHTML(animalInfo);

      const backBtn = listEl.querySelector('.animal-info-back-button');
      if (backBtn) backBtn.addEventListener('click', onBack);

      const exhibitHeading = listEl.querySelector('.animal-exhibit');
      if (exhibitHeading) {
         const viewBtn = document.createElement('button');
         viewBtn.className = 'view-on-map-button';
         viewBtn.textContent = 'View on Map';
         viewBtn.type = 'button';

         viewBtn.addEventListener('click', () => {
            const url = new URL('map.html', window.location.href);
            url.searchParams.set('focus', animalInfo.species || '');
            url.searchParams.set('exhibit', exhibitName || animalInfo.exhibit || '');
            window.location.href = url.toString();
         });

         exhibitHeading.insertAdjacentElement('afterend', viewBtn);
      }
   }

   return { render };
}