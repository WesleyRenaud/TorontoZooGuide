import { getOptionItemName, sortNamedOptions } from './namedItems.js';

function createPlaceholderOption(label) {
   const placeholder = document.createElement('option');
   placeholder.value = '';
   placeholder.textContent = label;
   return placeholder;
}

function createNamedOption(name) {
   const option = document.createElement('option');
   option.value = name;
   option.textContent = name;
   return option;
}

export function populateDropdown(selectEl, items, {
   emptyOptionLabel = 'Select an option',
   getName = item => String(item ?? '').trim(),
   sortItems = null,
} = {}) {
   if (selectEl?.tagName !== 'SELECT') {
      return;
   }

   const fragment = document.createDocumentFragment();
   fragment.appendChild(createPlaceholderOption(emptyOptionLabel));

   const resolvedItems = typeof sortItems === 'function'
      ? sortItems(items ?? [])
      : items ?? [];

   resolvedItems.forEach(item => {
      const name = getName(item);

      if (!name) return;

      fragment.appendChild(createNamedOption(name));
   });

   selectEl.replaceChildren(fragment);
}

export function populateValueDropdown(selectEl, values, emptyOptionLabel) {
   populateDropdown(selectEl, values, {
      emptyOptionLabel,
   });
}

function populateNamedDropdown(selectEl, items, emptyOptionLabel) {
   populateDropdown(selectEl, items, {
      emptyOptionLabel,
      getName: getOptionItemName,
      sortItems: sortNamedOptions,
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
