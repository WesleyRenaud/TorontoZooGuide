import { getActiveUpdateOptions } from '../../../api/consoleOperationsApi.js';

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

export async function loadActiveUpdates() {
   const result = await getActiveUpdateOptions();
   return result?.updates ?? [];
}

export function populateUpdateDropdown(selectEl, updates = []) {
   if (selectEl?.tagName !== 'SELECT') {
      return;
   }

   const fragment = document.createDocumentFragment();
   fragment.appendChild(createPlaceholderOption('Select an update'));

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

export function getSelectedUpdateIdentity(selectEl) {
   const selectedOption = selectEl?.selectedOptions?.[0] ?? null;

   return {
      title: selectedOption?.dataset?.title || '',
      startDate: selectedOption?.dataset?.startDate || '',
   };
}

export function getSelectedUpdateData(selectEl) {
   const selectedOption = selectEl?.selectedOptions?.[0] ?? null;

   return {
      ...getSelectedUpdateIdentity(selectEl),
      description: selectedOption?.dataset?.description || '',
      type: selectedOption?.dataset?.type || '',
      endDate: selectedOption?.dataset?.endDate || '',
   };
}
