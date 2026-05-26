import { APP_STRINGS } from '../../../strings.js';

export function createAnimalSpeciesResultsView({ inputEl, resultsEl } = {}) {
   let currentMatches = [];
   let highlightedIndex = -1;

   function renderResults(children = []) {
      resultsEl.replaceChildren(...children);
   }

   function clear() {
      renderResults();
      resultsEl.classList.remove('active');
      currentMatches = [];
      highlightedIndex = -1;
   }

   function updateHighlight() {
      const items = resultsEl.querySelectorAll('.console-operations-autocomplete-item');

      items.forEach((item, index) => {
         item.classList.toggle('is-highlighted', index === highlightedIndex);

         if (index === highlightedIndex) {
            item.scrollIntoView({ block: 'nearest' });
         }
      });
   }

   function selectSpecies(species) {
      inputEl.value = species;
      clear();
      inputEl.dispatchEvent(new Event('change', { bubbles: true }));
   }

   function render(matches) {
      currentMatches = matches;
      highlightedIndex = -1;

      if (!matches.length) {
         const empty = document.createElement('div');
         empty.className = 'console-operations-autocomplete-empty';
         empty.textContent = APP_STRINGS.common.noMatches;
         renderResults([empty]);
         resultsEl.classList.add('active');
         return;
      }

      const fragment = document.createDocumentFragment();

      matches.forEach((species) => {
         const item = document.createElement('button');
         item.type = 'button';
         item.className = 'console-operations-autocomplete-item';
         item.textContent = species;

         item.addEventListener('mousedown', (event) => {
            event.preventDefault();
         });

         item.addEventListener('click', () => {
            selectSpecies(species);
         });

         fragment.appendChild(item);
      });

      renderResults([fragment]);
      resultsEl.classList.add('active');
   }

   function handleKeydown(event) {
      const hasResults =
         resultsEl.classList.contains('active') &&
         currentMatches.length > 0;

      if (event.key === 'Escape') {
         clear();
         return;
      }

      if (!hasResults) {
         return;
      }

      if (event.key === 'ArrowDown') {
         event.preventDefault();
         highlightedIndex = Math.min(highlightedIndex + 1, currentMatches.length - 1);
         updateHighlight();
         return;
      }

      if (event.key === 'ArrowUp') {
         event.preventDefault();
         highlightedIndex = Math.max(highlightedIndex - 1, 0);
         updateHighlight();
         return;
      }

      if (event.key === 'Enter') {
         if (highlightedIndex >= 0 && highlightedIndex < currentMatches.length) {
            event.preventDefault();
            selectSpecies(currentMatches[highlightedIndex]);
         }
      }
   }

   return {
      clear,
      render,
      handleKeydown,
   };
}
