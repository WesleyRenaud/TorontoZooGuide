import { searchItineraryItems } from '../../api/searchApi.js';

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
}

function safeParse(raw, fallback) {
   try {
      return JSON.parse(raw);
   } catch {
      return fallback;
   }
}

function defaultMigrate(arr) {
   return Array.isArray(arr) ? arr : [];
}

function loadSelected(storageKey, migrate = defaultMigrate) {
   const raw = localStorage.getItem(storageKey);
   const arr = safeParse(raw || '[]', []);
   return migrate(arr);
}

function saveSelected(storageKey, selected) {
   localStorage.setItem(storageKey, JSON.stringify(selected));
}

export function createItinerarySelectorController({
   mountEl,

   onPrev,
   onNext,
   onFinish,
   onClose,
   hideNextButton = false,

   storageKey,
   migrateSelected = defaultMigrate,

   searchEndpoint = '/search',
   buildSearchPayload = (query) => ({ query }),
   extractRows = (res) =>
      (Array.isArray(res?.results) ? res.results :
       Array.isArray(res) ? res :
       []),

   getContext = null,

   getId,
   getTitle = () => '',
   getSubtitle = () => '',
   getImageSrc = () => null,
   getInfoLink = () => null,

   makeSelection = (row) => ({ id: getId(row) }),

   topTitle = 'Itinerary Builder',
   h1 = 'Add Items',
   subtitle = 'Search and add items to your plan.',
   emptyText = 'No results found.',

   renderRowLeft,
   renderExtraControls = null,

   onBeforeToggleAdd = null,
} = {}) {

   if (!storageKey) {
      throw new Error('createItinerarySelectorController: storageKey is required');
   }

   if (typeof getId !== 'function') {
      throw new Error('createItinerarySelectorController: getId(row) is required');
   }

   let root = null;
   let inputEl = null;
   let resultsEl = null;
   let bodyEl = null;

   let selected = loadSelected(storageKey, migrateSelected);

   function isSelected(id) {
      return selected.some(x => x && (x.id === id || x.species === id || x.name === id));
   }

   function toggleRow(row) {
      const id = getId(row);
      if (!id) return;

      if (isSelected(id)) {
         selected = selected.filter(x => (x?.id ?? x?.species ?? x?.name) !== id);
      } else {
         const sel = makeSelection(row) || {};
         if (!sel.id) sel.id = id;
         selected = [...selected, sel];
      }

      saveSelected(storageKey, selected);
   }

   function defaultRenderRowLeft(row) {
      const title = getTitle(row);
      const sub = getSubtitle(row);
      const src = getImageSrc(row);
      const infoLink = getInfoLink(row);

      const content = document.createElement('div');
      content.className = 'itin-animal-content';

      const thumbWrap = document.createElement('div');
      thumbWrap.className = 'itin-animal-thumb';

      if (src) {
         const img = document.createElement('img');
         img.className = 'itin-animal-thumb-img';
         img.loading = 'lazy';
         img.alt = title ? `${title} image` : '';
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
      titleEl.textContent = title || 'Item';
      left.appendChild(titleEl);

      if (sub) {
         const subEl = document.createElement('div');
         subEl.className = 'animal-result-exhibit';
         subEl.textContent = sub;
         left.appendChild(subEl);
      }

      if (infoLink) {
         const linkEl = document.createElement('a');
         linkEl.className = 'tooltip-link';
         linkEl.href = infoLink;
         linkEl.target = '_blank';
         linkEl.rel = 'noopener noreferrer';
         linkEl.textContent = 'More Info';

         linkEl.addEventListener('click', (e) => {
            e.stopPropagation();
         });

         left.appendChild(linkEl);
      }

      content.appendChild(thumbWrap);
      content.appendChild(left);

      return content;
   }

   function render(rows) {
      resultsEl.innerHTML = '';

      if (!Array.isArray(rows) || rows.length === 0) {
         const empty = document.createElement('div');
         empty.className = 'itin-empty';
         empty.textContent = emptyText;
         resultsEl.appendChild(empty);
         return;
      }

      rows.forEach(row => {
         const id = getId(row);

         const item = document.createElement('div');
         item.className = 'animal-result';

         const leftNode = (renderRowLeft || defaultRenderRowLeft)(row);

         const btn = document.createElement('button');
         btn.type = 'button';
         btn.className = 'itin-add-btn';

         const updateBtn = () => {
            const added = id && isSelected(id);
            btn.textContent = added ? '−' : '+';
            btn.classList.toggle('is-added', !!added);
         };

         const proceed = () => {
            toggleRow(row);
            updateBtn();
         };

         updateBtn();

         btn.addEventListener('click', (e) => {
            e.stopPropagation();

            const added = id && isSelected(id);

            if (typeof onBeforeToggleAdd === 'function') {
               onBeforeToggleAdd({
                  row,
                  id,
                  isSelected: !!added,
                  proceed,
               });
               return;
            }

            proceed();
         });

         item.appendChild(leftNode);
         item.appendChild(btn);

         resultsEl.appendChild(item);
      });
   }

   async function runSearch() {
      const query = (inputEl?.value ?? '').trim();

      try {
         const ctx =
            typeof getContext === 'function'
               ? await getContext()
               : {};

         const payload = {
            ...buildSearchPayload(query),
            ...ctx,
         };

         const response = await searchItineraryItems(searchEndpoint, payload);
         const rows = extractRows(response) || [];
         render(Array.isArray(rows) ? rows : []);
      } catch {
         render([]);
      }
   }

   function build() {
      root = document.createElement('div');
      root.className = 'itin-overlay';

      root.innerHTML = `
         <section class="itin-card itin-card-tall" role="dialog" aria-modal="true">
            <div class="itin-card-topbar itin-card-topbar-with-close">
               <div class="itin-top-title">${topTitle}</div>
               <button class="itin-close" type="button" aria-label="Close itinerary builder">×</button>
            </div>

            <div class="itin-card-body itin-card-body-tall">
               <h1 class="itin-h1">${h1}</h1>
               <p class="itin-subtitle">${subtitle}</p>

               <input
                  class="itin-search-input"
                  type="text"
                  placeholder="Search..."
                  autocomplete="off"
               />

               <div class="itin-results" aria-live="polite"></div>
            </div>

            <div class="itin-card-actions-dual">
               <button class="itin-prev" type="button">Previous</button>

               <div class="itin-actions-right">
                  ${hideNextButton ? '' : '<button class="itin-next" type="button">Next</button>'}
                  <button class="itin-finish" type="button">Finish</button>
               </div>
            </div>
         </section>
      `;

      bodyEl = root.querySelector('.itin-card-body');
      inputEl = root.querySelector('.itin-search-input');
      resultsEl = root.querySelector('.itin-results');

      if (typeof renderExtraControls === 'function') {
         renderExtraControls({
            rootEl: root,
            bodyEl,
            inputEl,
            resultsEl,
            rerunSearch: runSearch,
         });
      }

      inputEl.addEventListener('input', debounce(runSearch, 250));

      root
         .querySelector('.itin-prev')
         ?.addEventListener('click', () => onPrev?.());

      root
         .querySelector('.itin-next')
         ?.addEventListener('click', () => onNext?.(selected.slice()));

      root
         .querySelector('.itin-finish')
         ?.addEventListener('click', () => onFinish?.(selected.slice()));

      root
         .querySelector('.itin-close')
         ?.addEventListener('click', () => onClose?.());
   }

   function show() {
      if (!mountEl) return;

      if (!root) {
         build();
      }

      selected = loadSelected(storageKey, migrateSelected);

      mountEl.innerHTML = '';
      mountEl.appendChild(root);

      inputEl.value = '';
      runSearch();
   }

   function hide() {
      if (!mountEl) return;
      mountEl.innerHTML = '';
   }

   return {
      show,
      hide,
   };
}
