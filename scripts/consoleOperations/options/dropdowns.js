import { NamedItems } from './namedItems.js';
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

function populateNamedDropdown(selectEl, items, emptyOptionLabel) {
   Dropdowns.populateDropdown(selectEl, items, {
      emptyOptionLabel,
      getName: NamedItems.getOptionItemName,
      sortItems: NamedItems.sortNamedOptions,
   });
}

export class Dropdowns {
   static populateDropdown(selectEl, items, {
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

   static populateValueDropdown(selectEl, values, emptyOptionLabel) {
      Dropdowns.populateDropdown(selectEl, values, {
         emptyOptionLabel,
      });
   }

   static populateExhibitDropdown(selectEl, exhibits) {
      populateNamedDropdown(selectEl, exhibits, APP_STRINGS.placeholders.exhibit);
   }

   static populateRestaurantDropdown(selectEl, restaurants) {
      populateNamedDropdown(selectEl, restaurants, APP_STRINGS.placeholders.restaurant);
   }

   static populateRestroomDropdown(selectEl, restrooms) {
      populateNamedDropdown(selectEl, restrooms, APP_STRINGS.placeholders.restroom);
   }

   static populateGiftShopDropdown(selectEl, giftShops) {
      populateNamedDropdown(selectEl, giftShops, APP_STRINGS.placeholders.giftShop);
   }

   static populateAttractionDropdown(selectEl, attractions) {
      populateNamedDropdown(selectEl, attractions, APP_STRINGS.placeholders.attraction);
   }

   static populateTransportationStationDropdown(selectEl, transportationStations) {
      populateNamedDropdown(selectEl, transportationStations, APP_STRINGS.placeholders.transportationStation);
   }

   static populateGuardiansTalkDropdown(selectEl, guardiansTalks) {
      populateNamedDropdown(selectEl, guardiansTalks, APP_STRINGS.placeholders.talk);
   }

   static populateWildEncounterDropdown(selectEl, wildEncounters) {
      populateNamedDropdown(selectEl, wildEncounters, APP_STRINGS.placeholders.wildEncounter);
   }
}
