// scripts/itinerary/guardiansTalkSelector.js
import { ajaxPost } from '../utils/ajax.js';
import { normalizeParameter } from '../utils/normalize.js';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';
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

// Stored earlier by dateSelector as 'YYYY-MM-DD'
function getSavedISODate() {
   return localStorage.getItem(DATE_STORAGE_KEY) || '';
}

// Monday=1 ... Sunday=7
function isoDateToMonFirstDow(iso) {
   // Use noon local time to avoid timezone edge issues
   const d = iso ? new Date(`${iso}T12:00:00`) : new Date();
   if (!Number.isFinite(d.getTime())) return 1; // fallback Monday

   const js = d.getDay(); // Sun=0 ... Sat=6
   return js === 0 ? 7 : js; // Mon=1 ... Sun=7
}

// ✅ backend row helpers (match your API fields)
function getName(row) {
   return row.name ?? row.NAME ?? '';
}

function getLocation(row) {
   return row.location ?? row.LOCATION ?? '';
}

function getTimeOfDay(row) {
   return row.time_of_day ?? row.TIME_OF_DAY ?? '';
}

// Key must be unique per talk occurrence
function getKey(row, dayOfWeek) {
   const name = getName(row);
   const loc = getLocation(row);
   const time = getTimeOfDay(row);
   return `${name}||${loc}||${dayOfWeek}||${time}`;
}

// Images live at: ../images/meet-the-guardians-talks/[talk name].png
function buildTalkImageSrcFromName(name) {
   const file = normalizeParameter(name || '');
   if (!file) return null;
   return `../images/meet-the-guardians-talks/${file}.png`;
}

function buildStoredTalkObject(row, dayOfWeek) {
   const name = getName(row);
   const location = getLocation(row);
   const timeOfDay = getTimeOfDay(row);
   const key = getKey(row, dayOfWeek);

   return {
      key,
      name,
      location,
      dayOfWeek,
      timeOfDay,
      imageSrc: buildTalkImageSrcFromName(name),
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

export function createItineraryGuardiansTalkSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
} = {}) {
   let root = null;
   let inputEl = null;
   let resultsEl = null;

   let selected = loadSelected();
   let dayOfWeek = 1; // Mon=1..Sun=7

   function toggleTalk(talkObj) {
      if (!talkObj?.key) return;

      if (isSelected(selected, talkObj.key)) {
         selected = removeSelected(selected, talkObj.key);
      } else {
         // ✅ store full object
         selected = [...selected, talkObj];
      }

      saveSelected(selected);
   }

   function render(rows) {
      resultsEl.innerHTML = '';

      if (!Array.isArray(rows) || rows.length === 0) {
         const empty = document.createElement('div');
         empty.className = 'itin-empty';
         empty.textContent = 'No Meet the Guardians talks found for this day';
         resultsEl.appendChild(empty);
         return;
      }

      rows.forEach(row => {
         const talkObj = buildStoredTalkObject(row, dayOfWeek);
         const { key, name, location, timeOfDay, imageSrc } = talkObj;

         const item = document.createElement('div');
         item.className = 'animal-result'; // reuse the same row styling

         // left content: thumbnail + text
         const content = document.createElement('div');
         content.className = 'itin-animal-content';

         const thumbWrap = document.createElement('div');
         thumbWrap.className = 'itin-animal-thumb';

         if (imageSrc) {
            const img = document.createElement('img');
            img.className = 'itin-animal-thumb-img';
            img.loading = 'lazy';
            img.alt = name ? `${name} photo` : 'Talk photo';
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
         titleEl.textContent = name || 'Talk';
         left.appendChild(titleEl);

         // “Location • Time” line
         const meta = document.createElement('div');
         meta.className = 'itin-talk-meta';
         meta.textContent =
            `${location ? `Location: ${location}` : 'Location: —'}` +
            `${timeOfDay ? `  •  Time: ${timeOfDay}` : ''}`;
         left.appendChild(meta);

         content.appendChild(thumbWrap);
         content.appendChild(left);

         // plus / minus button
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
            toggleTalk(talkObj);
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
            includeMeetTheGuardiansTalks: true,
            dayOfWeek: dayOfWeek, // ✅ backend-friendly name
         });

         const rows = Array.isArray(response?.meet_the_guardians_talks)
            ? response.meet_the_guardians_talks
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
               <h1 class="itin-h1">Meet the Guardians</h1>
               <p class="itin-subtitle">Search and add talks to your plan.</p>

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

      root.querySelector('.itin-prev')?.addEventListener('click', () => {
         onPrev?.();
      });

      root.querySelector('.itin-next')?.addEventListener('click', () => {
         onNext?.(selectedObjectsOnly(selected));
      });

      root.querySelector('.itin-finish')?.addEventListener('click', () => {
         onFinish?.(selectedObjectsOnly(selected));
      });
   }

   function show() {
      if (!mountEl) return;
      if (!root) build();

      selected = loadSelected();

      // Use saved itinerary date to determine day-of-week
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