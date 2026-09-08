import { AnimalSpeciesAutocompleteHelper } from './animalSpeciesAutocompleteHelper.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { AnimalSpeciesResultsView } from '../autocomplete/animalSpeciesResultsView.js';
import { SpeciesMatcher } from '../autocomplete/speciesMatcher.js';
import { SpeciesProvider } from '../autocomplete/speciesProvider.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';

export class AnimalSpeciesController {
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

      const speciesSource = SpeciesProvider.createAnimalSpeciesSource();
      const resultsView = AnimalSpeciesResultsView.createAnimalSpeciesResultsView({
         inputEl,
         resultsEl,
      });

      let searchRequestId = 0;

      async function performSearch() {
         const query = ValueNormalizer.asTrimmedString(inputEl.value);
         const exhibit = ControllerHelper.getFieldValue(exhibitEl);
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

      const runSearch = AnimalSpeciesAutocompleteHelper.debounce(() => {
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
