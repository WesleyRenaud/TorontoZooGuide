import { ConsoleDropdownOptionBuilder } from '../../options/consoleDropdownOptionBuilder.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { Strings } from '../../../strings.js';

export class GuardiansTalkEnclosureDropdown {
   static reset(selectEl) {
      GuardiansTalkEnclosureDropdown.populate(selectEl, []);
   }

   static populate(selectEl, enclosureNames) {
      if (selectEl?.tagName !== 'SELECT') {
         return;
      }

      const hasChoice = enclosureNames.length > 1;

      selectEl.disabled = !hasChoice;
      selectEl.parentElement?.classList.toggle('is-invisible', !hasChoice);

      if (enclosureNames.length === 0) {
         selectEl.replaceChildren();
         selectEl.value = '';
         return;
      }

      if (!hasChoice) {
         const fragment = document.createDocumentFragment();
         fragment.appendChild(ConsoleDropdownOptionBuilder.createNamedOption(enclosureNames[0]));
         selectEl.replaceChildren(fragment);
         selectEl.value = enclosureNames[0];
         return;
      }

      ConsoleDropdownPopulator.populateValueDropdown(
         selectEl,
         enclosureNames,
         Strings.placeholders.enclosure
      );
      selectEl.value = '';
   }
}
