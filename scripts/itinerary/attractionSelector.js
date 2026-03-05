// scripts/itinerary/attractionSelector.js
import { ajaxPost } from '../utils/ajax.js';
import { normalizeParameter } from '../utils/normalize.js';

const STORAGE_KEY = 'tzg.itineraryAttractions';

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
}

function getAttractionName(row) {
   return (
      row.NAME ??
      row.name ??
      row.TITLE ??
      row.title ??
      row.ATTRACTION ??
      row.attraction ??
      ''
   );
}

function getInfoLink(row) {
   const v = row.info_link ?? row.INFO_LINK ?? row.infoLink ?? row.link ?? row.LINK ?? null;
   const s = typeof v === 'string' ? v.trim() : '';
   return s ? s : null;
}

function isFreeWithAdmission(row) {
   const v =
      row.free_with_admission ??
      row.FREE_WITH_ADMISSION ??
      row.freeWithAdmission ??
      row.is_free_with_admission ??
      row.IS_FREE_WITH_ADMISSION ??
      null;

   if (v === true) return true;
   if (v === false) return false;

   if (typeof v === 'number') return v !== 0;

   if (typeof v === 'string') {
      const s = v.trim().toLowerCase();
      if (['true', 't', 'yes', 'y', '1'].includes(s)) return true;
      if (['false', 'f', 'no', 'n', '0'].includes(s)) return false;
   }

   return false;
}

function getSubtitle(row) {
   return isFreeWithAdmission(row) ? 'Free With Admission' : 'Extra Charge';
}

/* ✅ flat images/attractions folder */
function buildAttractionImageSrc(row) {
   const name = getAttractionName(row);
   const nameFile = normalizeParameter(name || '');
   if (!nameFile) return null;
   return `../images/attractions/${nameFile}.png`;
}

function loadSelected() {
   try {
      const raw = localStorage.getItem(STORAGE_KEY);
      const arr = JSON.parse(raw || '[]');
      return Array.isArray(arr) ? arr : [];
   } catch {
      return [];
   }
}

function saveSelected(arr) {
   localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
}

/** stable id for selection */
function getId(obj) {
   const v = obj?.name ?? obj?.id ?? '';
   return typeof v === 'string' ? v : String(v);
}

/** back-compat: if old storage was strings, convert to objects */
function normalizeSelected(arr) {
   if (!Array.isArray(arr)) return [];
   return arr
      .map(x => {
         if (typeof x === 'string') return { name: x, imageSrc: null };
         return x;
      })
      .filter(x => getId(x));
}

export function createItineraryAttractionSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
} = {}) {
   let root = null;
   let inputEl = null;
   let resultsEl = null;
   let selected = normalizeSelected(loadSelected());

   function isSelected(id) {
      return selected.some(x => getId(x) === id);
   }

   function toggleAttraction(obj) {
      const id = getId(obj);
      if (!id) return;

      if (isSelected(id)) {
         selected = selected.filter(x => getId(x) !== id);
      } else {
         selected = [...selected, obj];
      }

      saveSelected(selected);
   }

   function render(rows) {
      resultsEl.innerHTML = '';

      if (!Array.isArray(rows) || rows.length === 0) {
         const empty = document.createElement('div');
         empty.className = 'itin-empty';
         empty.textContent = 'No attractions found.';
         resultsEl.appendChild(empty);
         return;
      }

      rows.forEach(row => {
         const name = getAttractionName(row);
         const subtitle = getSubtitle(row);
         const infoLink = getInfoLink(row);
         const imageSrc = buildAttractionImageSrc(row);

         const obj = {
            name,
            subtitle,
            freeWithAdmission: isFreeWithAdmission(row),
            infoLink,
            imageSrc,
         };

         const id = getId(obj);

         const item = document.createElement('div');
         item.className = 'animal-result'; // reuse styling

         // left content: thumbnail + text (and optional link)
         const content = document.createElement('div');
         content.className = 'itin-animal-content';

         const thumbWrap = document.createElement('div');
         thumbWrap.className = 'itin-animal-thumb';

         if (imageSrc) {
            const img = document.createElement('img');
            img.className = 'itin-animal-thumb-img';
            img.loading = 'lazy';
            img.alt = name ? `${name} photo` : 'Attraction photo';
            img.src = imageSrc;

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
         titleEl.textContent = name || 'Attraction';
         left.appendChild(titleEl);

         const subtitleEl = document.createElement('div');
         subtitleEl.className = 'animal-result-exhibit';
         subtitleEl.textContent = subtitle;
         left.appendChild(subtitleEl);

         // Optional info link
         if (infoLink) {
            const linkBtn = document.createElement('a');
            linkBtn.className = 'tooltip-link';
            linkBtn.href = infoLink;
            linkBtn.target = '_blank';
            linkBtn.rel = 'noopener noreferrer';
            linkBtn.textContent = 'More Info';
            linkBtn.style.display = 'inline-block';
            linkBtn.addEventListener('click', (e) => e.stopPropagation());
            left.appendChild(linkBtn);
         }

         content.appendChild(thumbWrap);
         content.appendChild(left);

         // plus / minus button
         const btn = document.createElement('button');
         btn.type = 'button';
         btn.className = 'itin-add-btn';

         const updateBtn = () => {
            const added = id && isSelected(id);
            btn.textContent = added ? '−' : '+';
            btn.classList.toggle('is-added', !!added);
         };

         updateBtn();

         btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleAttraction(obj);
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
         const response = await ajaxPost('/search', {
            query,
            includeAttractions: true,
         });

         const rows =
            Array.isArray(response?.attractions)
               ? response.attractions
               : Array.isArray(response)
               ? response
               : Array.isArray(response?.results)
               ? response.results
               : [];

         render(rows);
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
               <h1 class="itin-h1">Add Attractions</h1>
               <p class="itin-subtitle">Search and add attractions to your plan.</p>

               <input class="itin-search-input" type="text" placeholder="Search..." autocomplete="off" />

               <div class="itin-results" aria-live="polite"></div>
            </div>

            <div class="itin-card-actions-dual">
               <button class="itin-prev" type="button">Previous</button>
               <div class="itin-actions-right">
                  <button class="itin-next" type="button">Next</button>
                  <button class="itin-next itin-finish" type="button">Finish</button>
               </div>
            </div>
         </section>
      `;

      inputEl = root.querySelector('.itin-search-input');
      resultsEl = root.querySelector('.itin-results');

      inputEl.addEventListener('input', debounce(runSearch, 250));

      root.querySelector('.itin-prev')?.addEventListener('click', () => onPrev?.());

      root.querySelector('.itin-next')?.addEventListener('click', () => {
         // ✅ return full objects
         onNext?.(selected.slice());
      });

      root.querySelector('.itin-finish')?.addEventListener('click', () => {
         // ✅ same payload as Next, but lets main flow finalize immediately
         onFinish?.(selected.slice());
      });
   }

   function show() {
      if (!mountEl) return;
      if (!root) build();

      selected = normalizeSelected(loadSelected());

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