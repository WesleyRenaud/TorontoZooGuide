import {
   getOptionItemName,
   sortNamedOptions,
} from './namedItems.js';
import { APP_STRINGS } from '../../strings.js';

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
   emptyOptionLabel = APP_STRINGS.placeholders.option,
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
   populateNamedDropdown(selectEl, exhibits, APP_STRINGS.placeholders.exhibit);
}

export function populateRestaurantDropdown(selectEl, restaurants) {
   populateNamedDropdown(selectEl, restaurants, APP_STRINGS.placeholders.restaurant);
}

export function populateRestroomDropdown(selectEl, restrooms) {
   populateNamedDropdown(selectEl, restrooms, APP_STRINGS.placeholders.restroom);
}

export function populateGiftShopDropdown(selectEl, giftShops) {
   populateNamedDropdown(selectEl, giftShops, APP_STRINGS.placeholders.giftShop);
}

export function populateAttractionDropdown(selectEl, attractions) {
   populateNamedDropdown(selectEl, attractions, APP_STRINGS.placeholders.attraction);
}

export function populateZoomobileStationDropdown(selectEl, zoomobileStations) {
   populateNamedDropdown(selectEl, zoomobileStations, APP_STRINGS.placeholders.zoomobileStation);
}

export function populateGuardiansTalkDropdown(selectEl, guardiansTalks) {
   populateNamedDropdown(selectEl, guardiansTalks, APP_STRINGS.placeholders.talk);
}

export function populateWildEncounterDropdown(selectEl, wildEncounters) {
   populateNamedDropdown(selectEl, wildEncounters, APP_STRINGS.placeholders.wildEncounter);
}
