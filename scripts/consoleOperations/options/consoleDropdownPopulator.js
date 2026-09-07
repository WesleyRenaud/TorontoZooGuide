import { ConsoleDropdownOptionBuilder } from './consoleDropdownOptionBuilder.js';
import { Strings } from '../../strings.js';

export class ConsoleDropdownPopulator {
   static populateDropdown(selectEl, items, {
      emptyOptionLabel = Strings.placeholders.option,
      getName = item => String(item ?? '').trim(),
      sortItems = null,
   } = {}) {
      if (selectEl?.tagName !== 'SELECT') {
         return;
      }

      const fragment = document.createDocumentFragment();
      fragment.appendChild(ConsoleDropdownOptionBuilder.createPlaceholderOption(emptyOptionLabel));

      const resolvedItems = typeof sortItems === 'function'
         ? sortItems(items ?? [])
         : items ?? [];

      resolvedItems.forEach(item => {
         const name = getName(item);

         if (!name) return;

         fragment.appendChild(ConsoleDropdownOptionBuilder.createNamedOption(name));
      });

      selectEl.replaceChildren(fragment);
   }

   static populateValueDropdown(selectEl, values, emptyOptionLabel) {
      ConsoleDropdownPopulator.populateDropdown(selectEl, values, {
         emptyOptionLabel,
      });
   }

   static populateExhibitDropdown(selectEl, exhibits) {
      ConsoleDropdownOptionBuilder.populateNamedDropdown(selectEl, exhibits, Strings.placeholders.exhibit);
   }

   static populateRestaurantDropdown(selectEl, restaurants) {
      ConsoleDropdownOptionBuilder.populateNamedDropdown(selectEl, restaurants, Strings.placeholders.restaurant);
   }

   static populateRestroomDropdown(selectEl, restrooms) {
      ConsoleDropdownOptionBuilder.populateNamedDropdown(selectEl, restrooms, Strings.placeholders.restroom);
   }

   static populateGiftShopDropdown(selectEl, giftShops) {
      ConsoleDropdownOptionBuilder.populateNamedDropdown(selectEl, giftShops, Strings.placeholders.giftShop);
   }

   static populateAttractionDropdown(selectEl, attractions) {
      ConsoleDropdownOptionBuilder.populateNamedDropdown(selectEl, attractions, Strings.placeholders.attraction);
   }

   static populateTransportationStationDropdown(selectEl, transportationStations) {
      ConsoleDropdownOptionBuilder.populateNamedDropdown(selectEl, transportationStations, Strings.placeholders.transportationStation);
   }

   static populateGuardiansTalkDropdown(selectEl, guardiansTalks) {
      ConsoleDropdownOptionBuilder.populateNamedDropdown(selectEl, guardiansTalks, Strings.placeholders.talk);
   }

   static populateWildEncounterDropdown(selectEl, wildEncounters) {
      ConsoleDropdownOptionBuilder.populateNamedDropdown(selectEl, wildEncounters, Strings.placeholders.wildEncounter);
   }
}
