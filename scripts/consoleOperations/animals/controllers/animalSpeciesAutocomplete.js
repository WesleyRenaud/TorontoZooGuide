import { loadSpecies } from '../../utils.js';
import { postJson } from '../../../api/apiClient.js';

function debounce(fn, delay = 200) {
   let timer = null;

   return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), delay);
   };
}

function normalizeSpeciesList(species) {
   return [...new Set(
      (species || [])
         .map(s => String(s || '').trim())
         .filter(Boolean)
   )].sort((a, b) => a.localeCompare(b));
}

function filterSpecies(speciesList, query, maxResults = 12) {
   const q = String(query || '').trim().toLowerCase();

   if (!q) return [];

   const startsWithMatches = [];
   const containsMatches = [];

   speciesList.forEach(species => {
      const lower = species.toLowerCase();

      if (lower.startsWith(q)) {
         startsWithMatches.push(species);
      } else if (lower.includes(q)) {
         containsMatches.push(species);
      }
   });

   return [...startsWithMatches, ...containsMatches].slice(0, maxResults);
}

export function createAnimalSpeciesAutocompleteController({
   inputEl,
   resultsEl,
   exhibitEl = null,
} = {}) {
   if (!inputEl || !resultsEl) {
      return {
         clear: () => {},
      };
   }

   let allSpecies = [];
   let allSpeciesLoaded = false;
   let speciesByExhibit = new Map();
   let currentMatches = [];
   let highlightedIndex = -1;

   function clearResults() {
      resultsEl.innerHTML = '';
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
      clearResults();
   }

   function renderResults(matches) {
      resultsEl.innerHTML = '';
      currentMatches = matches;
      highlightedIndex = -1;

      if (!matches.length) {
         const empty = document.createElement('div');
         empty.className = 'console-operations-autocomplete-empty';
         empty.textContent = 'No matches';
         resultsEl.appendChild(empty);
         resultsEl.classList.add('active');
         return;
      }

      matches.forEach(species => {
         const item = document.createElement('button');
         item.type = 'button';
         item.className = 'console-operations-autocomplete-item';
         item.textContent = species;

         item.addEventListener('mousedown', e => {
            e.preventDefault();
         });

         item.addEventListener('click', () => {
            selectSpecies(species);
         });

         resultsEl.appendChild(item);
      });

      resultsEl.classList.add('active');
   }

   async function ensureAllSpeciesLoaded() {
      if (allSpeciesLoaded) return;

      const rawSpecies = await loadSpecies();
      allSpecies = normalizeSpeciesList(rawSpecies);
      allSpeciesLoaded = true;
   }

   async function loadSpeciesForExhibit(exhibit) {
      if (!exhibit) {
         await ensureAllSpeciesLoaded();
         return allSpecies;
      }

      if (speciesByExhibit.has(exhibit)) {
         return speciesByExhibit.get(exhibit);
      }

      const result = await postJson('/get-animals-in-exhibit', {
         exhibit
      });

      const animals = result?.animals ?? [];
      const species = normalizeSpeciesList(
         animals.map(animal => animal.species ?? animal.SPECIES ?? animal)
      );

      speciesByExhibit.set(exhibit, species);
      return species;
   }

   const runSearch = debounce(async () => {
      const query = inputEl.value.trim();
      const exhibit = exhibitEl?.value.trim() ?? '';

      if (query.length < 1) {
         clearResults();
         return;
      }

      try {
         const speciesList = await loadSpeciesForExhibit(exhibit);
         const matches = filterSpecies(speciesList, query);
         renderResults(matches);
      } catch (err) {
         clearResults();
      }
   }, 180);

   inputEl.addEventListener('input', () => {
      runSearch();
   });

   inputEl.addEventListener('focus', async () => {
      const query = inputEl.value.trim();
      const exhibit = exhibitEl?.value.trim() ?? '';

      if (!query) return;

      try {
         const speciesList = await loadSpeciesForExhibit(exhibit);
         const matches = filterSpecies(speciesList, query);
         renderResults(matches);
      } catch (err) {
         clearResults();
      }
   });

   inputEl.addEventListener('keydown', e => {
      const hasResults = resultsEl.classList.contains('active') && currentMatches.length > 0;

      if (e.key === 'Escape') {
         clearResults();
         return;
      }

      if (!hasResults) return;

      if (e.key === 'ArrowDown') {
         e.preventDefault();
         highlightedIndex = Math.min(highlightedIndex + 1, currentMatches.length - 1);
         updateHighlight();
         return;
      }

      if (e.key === 'ArrowUp') {
         e.preventDefault();
         highlightedIndex = Math.max(highlightedIndex - 1, 0);
         updateHighlight();
         return;
      }

      if (e.key === 'Enter') {
         if (highlightedIndex >= 0 && highlightedIndex < currentMatches.length) {
            e.preventDefault();
            selectSpecies(currentMatches[highlightedIndex]);
         }
      }
   });

   inputEl.addEventListener('blur', () => {
      setTimeout(() => {
         clearResults();
      }, 150);
   });

   exhibitEl?.addEventListener('change', () => {
      inputEl.value = '';
      clearResults();
   });

   return {
      clear: clearResults,
   };
}