import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { Strings } from '../../../strings.js';
import { UpdateOptionsFormatter } from './updateOptionsFormatter.js';

export class UpdateOptions {
   static async loadActiveUpdates() {
      const result = await ConsoleOperationsClient.getActiveUpdateOptions();
      return result?.updates ?? [];
   }

   static populateUpdateDropdown(selectEl, updates = [], placeholder = Strings.placeholders.update) {
      if (selectEl?.tagName !== 'SELECT') {
         return;
      }

      const fragment = document.createDocumentFragment();
      fragment.appendChild(UpdateOptionsFormatter.createPlaceholderOption(placeholder));

      updates.forEach((update) => {
         const optionEl = document.createElement('option');
         optionEl.value = JSON.stringify({
            title: update.title,
            startDate: update.start_date,
         });
         optionEl.textContent = UpdateOptionsFormatter.formatUpdateOptionLabel(update);
         optionEl.dataset.title = update.title || '';
         optionEl.dataset.startDate = update.start_date || '';
         optionEl.dataset.description = update.description || '';
         optionEl.dataset.type = update.type || '';
         optionEl.dataset.endDate = update.end_date || '';
         fragment.appendChild(optionEl);
      });

      selectEl.replaceChildren(fragment);
   }

   static populateClosureUpdateDropdown(selectEl, updates = []) {
      UpdateOptions.populateUpdateDropdown(
         selectEl,
         updates.filter((update) => update.type === 'Closure'),
         Strings.placeholders.closureUpdate,
      );
   }

   static getSelectedUpdateIdentity(selectEl) {
      const selectedOption = selectEl?.selectedOptions?.[0] ?? null;

      return {
         title: selectedOption?.dataset?.title || '',
         startDate: selectedOption?.dataset?.startDate || '',
      };
   }

   static getSelectedUpdateData(selectEl) {
      const selectedOption = selectEl?.selectedOptions?.[0] ?? null;

      return {
         ...UpdateOptions.getSelectedUpdateIdentity(selectEl),
         description: selectedOption?.dataset?.description || '',
         type: selectedOption?.dataset?.type || '',
         endDate: selectedOption?.dataset?.endDate || '',
      };
   }
}
