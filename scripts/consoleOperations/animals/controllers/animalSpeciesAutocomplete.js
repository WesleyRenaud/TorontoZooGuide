import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { createAnimalSpeciesResultsView } from '../autocomplete/resultsView.js';
import { SpeciesMatcher } from '../autocomplete/speciesMatcher.js';
import { createAnimalSpeciesSource } from '../autocomplete/speciesSource.js';
import { getFieldValue } from '../../helpers/controllerUtils.js';

function debounce(fn, delay = 200) {
   let timer = null;

   return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), delay);
   };
}

export class AnimalSpeciesAutocomplete {
   static createAnimalSpeciesAutocompleteController({
      inputEl,
      resultsEl,
      exhibitEl = null,
   } = {}) {
      if (!inputEl || !resultsEl) {
         return {
            clear: () => {},
         };
      }

      const speciesSource = createAnimalSpeciesSource();
      const resultsView = createAnimalSpeciesResultsView({
         inputEl,
         resultsEl,
      });

      let searchRequestId = 0;

      async function performSearch() {
         const query = ValueNormalizer.asTrimmedString(inputEl.value);
         const exhibit = getFieldValue(exhibitEl);
         const requestId = ++searchRequestId;

         if (!query) {
            resultsView.clear();
            return;
         }

         try {
            const speciesList = await speciesSource.loadForExhibit(exhibit);

            if (requestId !== searchRequestId) {
               return;
            }

            const matches = SpeciesMatcher.filterSpeciesMatches(speciesList, query);
            resultsView.render(matches);
         } catch (err) {
            if (requestId !== searchRequestId) {
               return;
            }

            resultsView.clear();
         }
      }

      const runSearch = debounce(() => {
         performSearch();
      }, 180);

      inputEl.addEventListener('input', () => {
         runSearch();
      });

      inputEl.addEventListener('focus', () => {
         if (!ValueNormalizer.asTrimmedString(inputEl.value)) {
            return;
         }

         performSearch();
      });

      inputEl.addEventListener('keydown', (event) => {
         resultsView.handleKeydown(event);
      });

      inputEl.addEventListener('blur', () => {
         setTimeout(() => {
            resultsView.clear();
         }, 150);
      });

      exhibitEl?.addEventListener('change', () => {
         searchRequestId += 1;
         inputEl.value = '';
         resultsView.clear();
      });

      return {
         clear: resultsView.clear,
      };
   }
}
