import { ConsoleDropdownPopulator } from './consoleDropdownPopulator.js';
import { NamedItems } from './namedItems.js';

export class ConsoleDropdownOptionBuilder {
   static createPlaceholderOption(label) {
      const placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = label;
      return placeholder;
   }

   static createNamedOption(name) {
      const option = document.createElement('option');
      option.value = name;
      option.textContent = name;
      return option;
   }

   static populateNamedDropdown(selectEl, items, emptyOptionLabel) {
      ConsoleDropdownPopulator.populateDropdown(selectEl, items, {
         emptyOptionLabel,
         getName: NamedItems.getOptionItemName,
         sortItems: NamedItems.sortNamedOptions,
      });
   }
}
