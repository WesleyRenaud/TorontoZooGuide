import { normalizeParameter } from '../utils/normalize.js';

export function buildSpeciesContentHTML(animal) {
   const section = (title, value) => {
      if (!value || !String(value).trim()) return '';
      return `
         <div class="section">
         <strong>${title}:</strong>
         <p>${value}</p>
         </div>
      `;
   };

   return `
      <img
         src="images/animals/${normalizeParameter(animal.exhibit)}/${normalizeParameter(animal.species)}.png"
         class="new-animal-image"
      >

      <h2 class="animal-species-name">${animal.species}</h2>
      ${animal.latin_name ? `<h6 class="latin-name">${animal.latin_name}</h6>` : ''}
      <h4 class="animal-exhibit">${animal.exhibit}</h4>

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