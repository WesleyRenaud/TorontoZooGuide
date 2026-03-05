// scripts/itinerary/animalSelector.js
import { ajaxPost } from '../utils/ajax.js';
import { normalizeParameter } from '../utils/normalize.js';

const STORAGE_KEY = 'tzg.itineraryAnimals';

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
}

function getSpecies(row) {
   return row.SPECIES ?? row.species ?? '';
}

function getExhibit(row) {
   return row.EXHIBIT ?? row.exhibit ?? '';
}

function getSubtitle(row) {
   const exhibit = getExhibit(row);
   return exhibit ? `Exhibit: ${exhibit}` : '';
}

function buildAnimalImageSrc(row) {
   const exhibit = getExhibit(row);
   const species = getSpecies(row);

   const exhibitFile = normalizeParameter(exhibit || '');
   const speciesFile = normalizeParameter(species || '');

   if (!exhibitFile || !speciesFile) return null;

   return `../images/animals/${exhibitFile}/${speciesFile}.png`;
}

/**
 * ✅ Selected animal shape (stored in localStorage)
 * {
 *   species: string,
 *   exhibit: string,
 *   imageSrc: string | null
 * }
 */

function migrateIfNeeded(arr) {
   if (!Array.isArray(arr)) return [];

   // Old format: ["Red Panda", "Amur Tiger"]
   if (arr.length > 0 && typeof arr[0] === 'string') {
      return arr
         .filter(Boolean)
         .map(species => ({ species, exhibit: '', imageSrc: null }));
   }

   // New-ish/unknown format: ensure consistent keys
   return arr
      .filter(x => x && typeof x === 'object')
      .map(x => ({
         species: x.species ?? x.SPECIES ?? '',
         exhibit: x.exhibit ?? x.EXHIBIT ?? '',
         imageSrc: x.imageSrc ?? x.image_src ?? x.image ?? null,
      }))
      .filter(x => x.species);
}

function loadSelected() {
   try {
      const raw = localStorage.getItem(STORAGE_KEY);
      const arr = JSON.parse(raw || '[]');
      return migrateIfNeeded(arr);
   } catch {
      return [];
   }
}

function saveSelected(arr) {
   localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
}

function isSelected(selectedArr, species) {
   if (!species) return false;
   return Array.isArray(selectedArr) && selectedArr.some(x => x?.species === species);
}

function makeAnimalSelection(row) {
   const species = getSpecies(row);
   const exhibit = getExhibit(row);
   const imageSrc = buildAnimalImageSrc(row); // ✅ store it once
   return { species, exhibit, imageSrc };
}

export function createItineraryAnimalSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish, // ✅ NEW
} = {}) {
   let root = null;
   let inputEl = null;
   let resultsEl = null;
   let selected = loadSelected();

   function toggleAnimal(row) {
      const species = getSpecies(row);
      if (!species) return;

      if (isSelected(selected, species)) {
         selected = selected.filter(x => x?.species !== species);
      } else {
         selected = [...selected, makeAnimalSelection(row)];
      }

      saveSelected(selected);
   }

   function render(rows) {
      resultsEl.innerHTML = '';

      if (!Array.isArray(rows) || rows.length === 0) {
         const empty = document.createElement('div');
         empty.className = 'itin-empty';
         empty.textContent = 'No animals found.';
         resultsEl.appendChild(empty);
         return;
      }

      rows.forEach(row => {
         const species = getSpecies(row);
         const subtitle = getSubtitle(row);

         const item = document.createElement('div');
         item.className = 'animal-result';

         // left content: thumbnail + text
         const content = document.createElement('div');
         content.className = 'itin-animal-content';

         const thumbWrap = document.createElement('div');
         thumbWrap.className = 'itin-animal-thumb';

         const src = buildAnimalImageSrc(row);
         if (src) {
            const img = document.createElement('img');
            img.className = 'itin-animal-thumb-img';
            img.loading = 'lazy';
            img.alt = species ? `${species} photo` : 'Animal photo';
            img.src = src;

            img.addEventListener('error', () => {
               thumbWrap.classList.add('is-placeholder');
               img.remove();
            });

            thumbWrap.appendChild(img);
         } else {
            thumbWrap.classList.add('is-placeholder');
         }

         const left = document.createElement('div');
         left.className = 'animal-result-left';

         const titleEl = document.createElement('div');
         titleEl.className = 'animal-result-species';
         titleEl.textContent = species || 'Animal';
         left.appendChild(titleEl);

         if (subtitle) {
            const subtitleEl = document.createElement('div');
            subtitleEl.className = 'animal-result-exhibit';
            subtitleEl.textContent = subtitle;
            left.appendChild(subtitleEl);
         }

         content.appendChild(thumbWrap);
         content.appendChild(left);

         // plus / minus button
         const btn = document.createElement('button');
         btn.type = 'button';
         btn.className = 'itin-add-btn';

         const updateBtn = () => {
            const added = species && isSelected(selected, species);
            btn.textContent = added ? '−' : '+';
            btn.classList.toggle('is-added', !!added);
         };

         updateBtn();

         btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleAnimal(row); // ✅ store full object (incl. imageSrc)
            updateBtn();
         });

         item.appendChild(content);
         item.appendChild(btn);
         resultsEl.appendChild(item);
      });
   }

   async function runSearch() {
      const query = (inputEl?.value ?? '').trim();

      try {
         const response = await ajaxPost('/search', { query, includeAnimals: true });

         const rows =
            (Array.isArray(response?.animals)
               ? response.animals
               : Array.isArray(response)
               ? response
               : response?.results) || [];

         render(Array.isArray(rows) ? rows : []);
      } catch {
         render([]);
      }
   }

   function build() {
      root = document.createElement('div');
      root.className = 'itin-overlay';
      root.innerHTML = `
         <section class="itin-card itin-card-tall" role="dialog" aria-modal="true" aria-label="Itinerary Builder">
            <div class="itin-card-topbar">
               <div class="itin-top-title">Itinerary Builder</div>
            </div>

            <div class="itin-card-body itin-card-body-tall">
               <h1 class="itin-h1">Add Animals</h1>
               <p class="itin-subtitle">Search and add animals to your plan.</p>

               <input class="itin-search-input" type="text" placeholder="Search..." autocomplete="off" />

               <div class="itin-results" aria-live="polite"></div>
            </div>

            <div class="itin-card-actions-dual">
               <button class="itin-prev" type="button">Previous</button>
               <div class="itin-actions-right">
                  <button class="itin-next" type="button">Next</button>
                  <button class="itin-finish" type="button">Finish</button>
               </div>
            </div>
         </section>
      `;

      inputEl = root.querySelector('.itin-search-input');
      resultsEl = root.querySelector('.itin-results');

      inputEl.addEventListener('input', debounce(runSearch, 250));

      root.querySelector('.itin-prev')?.addEventListener('click', () => {
         onPrev?.();
      });

      root.querySelector('.itin-next')?.addEventListener('click', () => {
         onNext?.(selected.slice());
      });

      root.querySelector('.itin-finish')?.addEventListener('click', () => {
         onFinish?.(selected.slice());
      });
   }

   function show() {
      if (!mountEl) return;
      if (!root) build();

      selected = loadSelected();

      mountEl.innerHTML = '';
      mountEl.appendChild(root);

      inputEl.value = '';
      runSearch();
   }

   function hide() {
      if (!mountEl) return;
      mountEl.innerHTML = '';
   }

   return { show, hide };
}