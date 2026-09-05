import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { APP_STRINGS } from '../../../strings.js';

function createPlaceholderOption(label) {
   const optionEl = document.createElement('option');
   optionEl.value = '';
   optionEl.textContent = label;
   return optionEl;
}

function formatDateRange(update) {
   if (!update.end_date) {
      return `${update.start_date} onward`;
   }

   return `${update.start_date} to ${update.end_date}`;
}

function formatUpdateOptionLabel(update) {
   return `${update.title} (${update.type}, ${formatDateRange(update)})`;
}

export class UpdateOptions {
   static async loadActiveUpdates() {
      const result = await ConsoleOperationsApi.getActiveUpdateOptions();
      return result?.updates ?? [];
   }

   static populateUpdateDropdown(selectEl, updates = []) {
      if (selectEl?.tagName !== 'SELECT') {
         return;
      }

      const fragment = document.createDocumentFragment();
      fragment.appendChild(createPlaceholderOption(APP_STRINGS.placeholders.update));

      updates.forEach((update) => {
         const optionEl = document.createElement('option');
         optionEl.value = JSON.stringify({
            title: update.title,
            startDate: update.start_date,
         });
         optionEl.textContent = formatUpdateOptionLabel(update);
         optionEl.dataset.title = update.title || '';
         optionEl.dataset.startDate = update.start_date || '';
         optionEl.dataset.description = update.description || '';
         optionEl.dataset.type = update.type || '';
         optionEl.dataset.endDate = update.end_date || '';
         fragment.appendChild(optionEl);
      });

      selectEl.replaceChildren(fragment);
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
