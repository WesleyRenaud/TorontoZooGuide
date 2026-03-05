import { ajaxPost } from '../utils/ajax.js';
import { normalizeParameter } from '../utils/normalize.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';
const DATE_STORAGE_KEY = 'tzg.itineraryDateISO';

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
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

function getSavedISODate() {
   return localStorage.getItem(DATE_STORAGE_KEY) || '';
}

// Monday=1 ... Sunday=7
function isoDateToMonFirstDow(iso) {
   const d = iso ? new Date(`${iso}T12:00:00`) : new Date();
   const js = d.getDay();
   return js === 0 ? 7 : js;
}

/* =========================
   Row field helpers
========================= */

function getName(row) {
   return row.name ?? row.NAME ?? '';
}

function getMeetingSpot(row) {
   return (
      row.meeting_spot ??
      row.MEETING_SPOT ??
      row.meetingSpot ??
      row.MEETINGSPOT ??
      row.location ??
      row.LOCATION ??
      ''
   );
}

function getTimeOfDay(row) {
   return row.time_of_day ?? row.TIME_OF_DAY ?? row.time ?? row.TIME ?? '';
}

function getLink(row) {
   const v = row.link ?? row.LINK ?? row.info_link ?? row.INFO_LINK ?? null;
   const s = typeof v === 'string' ? v.trim() : '';
   return s ? s : null;
}

function getKey(row, dayOfWeek) {
   const name = getName(row);
   const spot = getMeetingSpot(row);
   const time = getTimeOfDay(row);
   return `${name}||${spot}||${dayOfWeek}||${time}`;
}

function buildWildEncounterImageSrcFromName(name) {
   const file = normalizeParameter(name || '');
   if (!file) return null;
   return `../images/wild-encounters/${file}.png`;
}

function buildStoredWildEncounterObject(row, dayOfWeek) {
   const name = getName(row);
   const meetingSpot = getMeetingSpot(row);
   const timeOfDay = getTimeOfDay(row);
   const link = getLink(row);
   const key = getKey(row, dayOfWeek);

   return {
      key,
      name,
      meetingSpot,
      dayOfWeek,
      timeOfDay,
      link,
      imageSrc: buildWildEncounterImageSrcFromName(name),
   };
}

function isSelected(selectedArr, key) {
   return selectedArr.some(x => (typeof x === 'string' ? x === key : x?.key === key));
}

function removeSelected(selectedArr, key) {
   return selectedArr.filter(x => (typeof x === 'string' ? x !== key : x?.key !== key));
}

function selectedObjectsOnly(selectedArr) {
   return (Array.isArray(selectedArr) ? selectedArr : [])
      .map(x => (typeof x === 'string' ? null : x))
      .filter(Boolean);
}

export function createItineraryWildEncounterSelectorController({
   mountEl,
   onPrev,
   onFinish,
} = {}) {
   let root = null;
   let inputEl = null;
   let resultsEl = null;

   let selected = loadSelected();
   let dayOfWeek = 1;

   function toggleEncounter(encObj) {
      if (!encObj?.key) return;

      if (isSelected(selected, encObj.key)) {
         selected = removeSelected(selected, encObj.key);
      } else {
         selected = [...selected, encObj];
      }

      saveSelected(selected);
   }

   function render(rows) {
      resultsEl.innerHTML = '';

      if (!Array.isArray(rows) || rows.length === 0) {
         const empty = document.createElement('div');
         empty.className = 'itin-empty';
         empty.textContent = 'No wild encounters found for this day';
         resultsEl.appendChild(empty);
         return;
      }

      rows.forEach(row => {
         const encObj = buildStoredWildEncounterObject(row, dayOfWeek);
         const { key, name, meetingSpot, timeOfDay, link, imageSrc } = encObj;

         const item = document.createElement('div');
         item.className = 'animal-result';

         const content = document.createElement('div');
         content.className = 'itin-animal-content';

         const thumbWrap = document.createElement('div');
         thumbWrap.className = 'itin-animal-thumb';

         if (imageSrc) {
            const img = document.createElement('img');
            img.className = 'itin-animal-thumb-img';
            img.loading = 'lazy';
            img.alt = name ? `${name} photo` : 'Wild encounter photo';
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
         titleEl.textContent = name || 'Wild Encounter';
         left.appendChild(titleEl);

         const meta = document.createElement('div');
         meta.className = 'itin-talk-meta';
         meta.textContent =
            `${meetingSpot ? `Meeting Spot: ${meetingSpot}` : 'Meeting Spot: —'}` +
            `${timeOfDay ? `  •  Time: ${timeOfDay}` : ''}`;
         left.appendChild(meta);

         if (link) {
            const a = document.createElement('a');
            a.className = 'tooltip-link';
            a.textContent = 'More Info';
            a.href = link;
            a.target = '_blank';
            a.rel = 'noopener noreferrer';
            a.addEventListener('click', (e) => e.stopPropagation());
            left.appendChild(a);
         }

         content.appendChild(thumbWrap);
         content.appendChild(left);

         const btn = document.createElement('button');
         btn.type = 'button';
         btn.className = 'itin-add-btn';

         const updateBtn = () => {
            const added = key && isSelected(selected, key);
            btn.textContent = added ? '−' : '+';
            btn.classList.toggle('is-added', !!added);
         };

         updateBtn();

         btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleEncounter(encObj);
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
            dayOfWeek,
            includeWildEncounters: true,
         });

         const rows = Array.isArray(response?.wild_encounters)
            ? response.wild_encounters
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
               <h1 class="itin-h1">Wild Encounters</h1>
               <p class="itin-subtitle">Search and add wild encounters to your plan.</p>

               <input class="itin-search-input" type="text" placeholder="Search..." autocomplete="off" />
               <div class="itin-results" aria-live="polite"></div>
            </div>

            <div class="itin-card-actions-dual">
               <button class="itin-prev" type="button">Previous</button>
               <button class="itin-next itin-finish" type="button">Finish</button>
            </div>
         </section>
      `;

      inputEl = root.querySelector('.itin-search-input');
      resultsEl = root.querySelector('.itin-results');

      inputEl.addEventListener('input', debounce(runSearch, 250));

      root.querySelector('.itin-prev')?.addEventListener('click', () => onPrev?.());

      root.querySelector('.itin-finish')?.addEventListener('click', () => {
         onFinish?.(selectedObjectsOnly(selected));
      });
   }

   function show() {
      if (!mountEl) return;
      if (!root) build();

      selected = loadSelected();

      const iso = getSavedISODate();
      dayOfWeek = isoDateToMonFirstDow(iso);

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