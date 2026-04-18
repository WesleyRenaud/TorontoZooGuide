import { getOptionItemName, sortNamedOptions } from './namedItems.js';

function populateNamedDropdown(selectEl, items, emptyOptionLabel) {
   if (!selectEl) return;

   selectEl.innerHTML = '';

   const placeholder = document.createElement('option');
   placeholder.value = '';
   placeholder.textContent = emptyOptionLabel;
   selectEl.appendChild(placeholder);

   sortNamedOptions(items).forEach(item => {
      const name = getOptionItemName(item);

      if (!name) return;

      const option = document.createElement('option');
      option.value = name;
      option.textContent = name;
      selectEl.appendChild(option);
   });
}

export function populateExhibitDropdown(selectEl, exhibits) {
   populateNamedDropdown(selectEl, exhibits, 'Select an exhibit');
}

export function populateRestaurantDropdown(selectEl, restaurants) {
   populateNamedDropdown(selectEl, restaurants, 'Select a restaurant');
}

export function populateGiftShopDropdown(selectEl, giftShops) {
   populateNamedDropdown(selectEl, giftShops, 'Select a gift shop');
}

export function populateAttractionDropdown(selectEl, attractions) {
   populateNamedDropdown(selectEl, attractions, 'Select an attraction');
}

export function populateZoomobileStationDropdown(selectEl, zoomobileStations) {
   populateNamedDropdown(selectEl, zoomobileStations, 'Select a zoomobile station');
}

export function populateGuardiansTalkDropdown(selectEl, guardiansTalks) {
   populateNamedDropdown(selectEl, guardiansTalks, 'Select a talk');
}

export function populateWildEncounterDropdown(selectEl, wildEncounters) {
   populateNamedDropdown(selectEl, wildEncounters, 'Select a Wild Encounter');
}
