// scripts/itinerary/itineraryRenderer.js
const ITIN_KEY = 'tzg.itinerary';
const DATE_KEY = 'tzg.itineraryDateISO';

const ANIMALS_KEY = 'tzg.itineraryAnimals';
const ATTRACTIONS_KEY = 'tzg.itineraryAttractions';
const GUARDIANS_KEY = 'tzg.itineraryGuardiansTalks';
const WILD_KEY = 'tzg.itineraryWildEncounters';

function el(tag, className, text) {
   const node = document.createElement(tag);
   if (className) node.className = className;
   if (text != null) node.textContent = text;
   return node;
}

function safeImg(src) {
   const img = document.createElement('img');
   img.src = src;
   img.alt = '';
   img.loading = 'lazy';
   img.onerror = () => { img.style.display = 'none'; };
   return img;
}

function safeParseJSON(raw, fallback) {
   try {
      return JSON.parse(raw);
   } catch {
      return fallback;
   }
}

function asString(x) {
   if (x == null) return '';
   return typeof x === 'string' ? x : String(x);
}

function formatISODateLong(iso) {
   if (!iso || typeof iso !== 'string') return '';
   const d = new Date(`${iso}T12:00:00`);
   if (!Number.isFinite(d.getTime())) return '';
   return d.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
   });
}

function clearItineraryStorage() {
   localStorage.removeItem(ITIN_KEY);
   localStorage.removeItem(DATE_KEY);

   // Clear step storage too (so rebuild is clean)
   localStorage.removeItem(ANIMALS_KEY);
   localStorage.removeItem(ATTRACTIONS_KEY);
   localStorage.removeItem(GUARDIANS_KEY);
   localStorage.removeItem(WILD_KEY);

   window.dispatchEvent(new CustomEvent('tzg:itineraryUpdated'));
}

function makeSection({ title, count, children }) {
   const section = el('section', 'itin-panel-section');

   const header = el('div', 'itin-panel-section-header');
   const titleEl = el('div', 'itin-panel-section-title');
   titleEl.appendChild(document.createTextNode(title));

   const countEl = el('span', 'itin-panel-count', `(${count})`);
   titleEl.appendChild(countEl);

   const toggleBtn = el('button', 'itin-panel-toggle');
   toggleBtn.type = 'button';
   toggleBtn.setAttribute('aria-label', `Toggle ${title}`);
   toggleBtn.appendChild(el('span', 'itin-panel-toggle-icon'));

   header.appendChild(titleEl);
   header.appendChild(toggleBtn);

   const body = el('div', 'itin-panel-section-body');
   children.forEach(child => body.appendChild(child));

   const toggle = () => section.classList.toggle('is-collapsed');
   header.addEventListener('click', toggle);
   toggleBtn.addEventListener('click', (e) => { e.stopPropagation(); toggle(); });

   section.appendChild(header);
   section.appendChild(body);
   return section;
}

function makeItemRow({ name, imageSrc, metaLines = [], linkText, onLinkClick }) {
   const row = el('div', 'itin-panel-item');

   const left = el('div', 'itin-panel-item-left');

   const thumb = el('div', 'itin-panel-thumb');
   if (imageSrc) thumb.appendChild(safeImg(imageSrc));
   left.appendChild(thumb);

   const text = el('div', 'itin-panel-text');
   text.appendChild(el('div', 'itin-panel-name', name));

   metaLines.forEach(line => {
      if (!line) return;
      text.appendChild(el('div', 'itin-panel-meta', line));
   });

   if (linkText) {
      const link = el('div', 'itin-panel-link', linkText);
      link.addEventListener('click', (e) => {
         e.stopPropagation();
         onLinkClick?.();
      });
      text.appendChild(link);
   }

   left.appendChild(text);
   row.appendChild(left);

   return row;
}

// Back-compat helpers in case any older storage still contains strings
function normalizeAnimal(a) {
   if (typeof a === 'string') return { species: a };
   return a && typeof a === 'object' ? a : { species: asString(a) };
}

function normalizeAttraction(a) {
   if (typeof a === 'string') return { name: a };
   return a && typeof a === 'object' ? a : { name: asString(a) };
}

function normalizeTalk(t) {
   if (typeof t === 'string') return { name: t };
   return t && typeof t === 'object' ? t : { name: asString(t) };
}

function normalizeWild(w) {
   if (typeof w === 'string') return { name: w };
   return w && typeof w === 'object' ? w : { name: asString(w) };
}

function renderBuildOnly(body) {
   const wrap = el('div', 'itin-panel-actions-wrap');
   const buildBtn = el('button', 'itin-panel-build-btn', 'Build Itinerary');
   buildBtn.type = 'button';
   buildBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('tzg:editItinerary'));
   });
   wrap.appendChild(buildBtn);
   body.appendChild(wrap);
}

export function renderItineraryPanel() {
   const body = document.getElementById('itineraryPanelBody');
   if (!body) return;

   body.innerHTML = '';

   const raw = localStorage.getItem(ITIN_KEY);
   if (!raw) {
      renderBuildOnly(body);
      return;
   }

   const itin = safeParseJSON(raw, null);
   if (!itin) {
      renderBuildOnly(body);
      return;
   }

   const animals = Array.isArray(itin.animals) ? itin.animals : [];
   const attractions = Array.isArray(itin.attractions) ? itin.attractions : [];
   const guardiansTalks = Array.isArray(itin.guardiansTalks) ? itin.guardiansTalks : [];
   const wildEncounters = Array.isArray(itin.wildEncounters) ? itin.wildEncounters : [];

   if (!animals.length && !attractions.length && !guardiansTalks.length && !wildEncounters.length) {
      renderBuildOnly(body);
      return;
   }

   // ✅ Action bar (separate from date card): Edit + Clear
   const actionsWrap = el('div', 'itin-panel-actions-wrap');

   const editBtn = el('button', 'itin-panel-edit-btn', 'Edit Itinerary');
   editBtn.type = 'button';
   editBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.dispatchEvent(new CustomEvent('tzg:editItinerary'));
   });

   const clearBtn = el('button', 'itin-panel-clear-btn', 'Clear');
   clearBtn.type = 'button';
   clearBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const ok = window.confirm('Clear your itinerary? This will remove all selected items.');
      if (!ok) return;
      clearItineraryStorage();
      renderItineraryPanel();
   });

   actionsWrap.appendChild(editBtn);
   actionsWrap.appendChild(clearBtn);
   body.appendChild(actionsWrap);

   // ✅ Visit Date card (separate module)
   const dateISO = itin.dateISO || localStorage.getItem(DATE_KEY) || '';
   const prettyDate = formatISODateLong(dateISO);

   if (prettyDate) {
      const dateWrap = el('div', 'itin-panel-date');
      dateWrap.appendChild(el('div', 'itin-panel-date-label', 'Visit Date'));
      dateWrap.appendChild(el('div', 'itin-panel-date-value', prettyDate));
      body.appendChild(dateWrap);
   }

   // ✅ Animals: render stored object (including stored imageSrc)
   const animalRows = animals.map(rawAnimal => {
      const a = normalizeAnimal(rawAnimal);

      const name = a.species ?? a.SPECIES ?? a.name ?? a.species_name ?? 'Animal';
      const exhibit = a.exhibit ?? a.EXHIBIT ?? a.exhibit_name ?? '';
      const imageSrc = a.imageSrc ?? a.image_src ?? a.image ?? null;
      const link = a.link ?? a.infoLink ?? a.INFO_LINK ?? null;

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [exhibit ? `Exhibit: ${exhibit}` : ''],
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });

   // ✅ Attractions: render stored object (including stored imageSrc)
   const attractionRows = attractions.map(rawAttr => {
      const x = normalizeAttraction(rawAttr);

      const name = x.name ?? x.NAME ?? 'Attraction';
      const subtitle = x.subtitle ?? '';
      const imageSrc = x.imageSrc ?? x.image_src ?? null;
      const infoLink = x.infoLink ?? x.info_link ?? x.link ?? x.LINK ?? null;

      const location = x.location ?? '';
      const price = x.price ?? '';

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            subtitle || '',
            location ? `Location: ${location}` : '',
            price ? `Price: ${price}` : '',
         ],
         linkText: infoLink ? 'More Info' : null,
         onLinkClick: infoLink ? () => window.open(infoLink, '_blank') : null,
      });
   });

   // ✅ Meet the Guardians: render stored fields (location/time/link/imageSrc)
   const guardiansRows = guardiansTalks.map(rawTalk => {
      const t = normalizeTalk(rawTalk);

      const name = t.name ?? t.NAME ?? 'Talk';
      const location = t.location ?? t.LOCATION ?? '';
      const time = t.time_of_day ?? t.TIME_OF_DAY ?? t.time ?? t.TIME ?? '';
      const link = t.link ?? t.LINK ?? t.infoLink ?? t.info_link ?? null;

      const imageSrc =
         t.imageSrc ??
         t.image_src ??
         (name ? `../images/meet-the-guardians-talks/${name}.png` : null);

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            location ? `Location: ${location}` : '',
            time ? `Time: ${time}` : '',
         ],
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });

   // ✅ Wild Encounters: render stored fields (meeting spot/time/link/imageSrc)
   const wildRows = wildEncounters.map(rawWild => {
      const w = normalizeWild(rawWild);

      const name = w.name ?? w.NAME ?? 'Wild Encounter';
      const meetingSpot =
         w.meeting_spot ?? w.MEETING_SPOT ?? w.meetingSpot ?? w.location ?? w.LOCATION ?? '';
      const time = w.time_of_day ?? w.TIME_OF_DAY ?? w.time ?? w.TIME ?? '';
      const link = w.link ?? w.LINK ?? w.infoLink ?? w.info_link ?? null;

      const imageSrc =
         w.imageSrc ??
         w.image_src ??
         (name ? `../images/wild-encounters/${name}.png` : null);

      return makeItemRow({
         name,
         imageSrc,
         metaLines: [
            meetingSpot ? `Meeting Spot: ${meetingSpot}` : '',
            time ? `Time: ${time}` : '',
         ],
         linkText: link ? 'More Info' : null,
         onLinkClick: link ? () => window.open(link, '_blank') : null,
      });
   });

   if (animals.length) body.appendChild(makeSection({ title: 'Animals', count: animals.length, children: animalRows }));
   if (attractions.length) body.appendChild(makeSection({ title: 'Attractions', count: attractions.length, children: attractionRows }));
   if (guardiansTalks.length) body.appendChild(makeSection({ title: 'Meet the Guardians', count: guardiansTalks.length, children: guardiansRows }));
   if (wildEncounters.length) body.appendChild(makeSection({ title: 'Wild Encounters', count: wildEncounters.length, children: wildRows }));
}