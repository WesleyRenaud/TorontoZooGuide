// ============================================================
// scripts.js
// - Map markers + tooltip carousel
// - Map preset (summer/winter/specific-day) + date picker
// - Search animals + inline "View on Map" (NO page reload)
// - Focus flow supports both:
//    1) URL ?focus=... (optional deep-linking)
//    2) search results button (stays on page)
// ============================================================

/* ============================================================
   CONFIG
============================================================ */

const apiKey = '657afbbbe68b892616c765dce8e68d6b';
const lat = 43.8177;
const lon = -79.1859;

/* ============================================================
   GLOBAL STATE
============================================================ */

let mapPanzoom = null;
let lastAnimals = [];
let markerElsByCoord = new Map(); // key: "x|y" -> marker element

const DEFAULT_CONTAIN = 'outside';
const FOCUS_CONTAIN = 'none';

const tooltip = document.getElementById('tooltip');

/* ============================================================
   PAGE HELPERS
============================================================ */

function getPageName() {
   return window.location.pathname.split('/').pop().replace('.html', '');
}

function getQueryParam(name) {
   return new URLSearchParams(window.location.search).get(name);
}

function setContain(mode) {
   if (!mapPanzoom) return;

   if (mapPanzoom.options) {
      mapPanzoom.options.contain = mode;
   }

   if (typeof mapPanzoom.setOptions === 'function') {
      mapPanzoom.setOptions({ contain: mode });
   }
}

/* ============================================================
   INIT
============================================================ */

document.addEventListener('DOMContentLoaded', () => {
   if (getPageName() !== 'map') return;
   initMapPage();
});

function initMapPage() {
   TooltipController.initGlobalListeners();

   const mapInner = document.getElementById('mapInner');
   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');
   const includeOffDisplayCheckbox = document.getElementById('includeOffDisplayAnimals');
   const animalSearchInput = document.getElementById('animalSearch');

   if (!mapInner || !mapPreset || !mapDateInput) return;

   mapPanzoom = initPanzoom(mapInner);
   initMapControls(mapPreset, mapDateInput, includeOffDisplayCheckbox);
   initAnimalSearch(animalSearchInput);

   // Optional deep-link support (?focus=...)
   initFocusFromQuery();
}

/* ============================================================
   PANZOOM
============================================================ */

function initPanzoom(mapInner) {
   const panzoom = Panzoom(mapInner, {
      maxScale: 10,
      minScale: 1,
      contain: DEFAULT_CONTAIN,
   });

   mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

   const regionLabels = document.querySelectorAll('.region-label');
   const exhibitLabels = document.querySelectorAll('.exhibit-label');

   const regionHideZoomScale = 1.5;
   const exhibitHideZoomScale = 2;

   mapInner.addEventListener('panzoomchange', () => {
      const currentScale = panzoom.getScale();

      regionLabels.forEach(label => {
         label.style.display = currentScale > regionHideZoomScale ? 'none' : 'block';
      });

      exhibitLabels.forEach(label => {
         label.style.display = currentScale > exhibitHideZoomScale ? 'none' : 'block';
      });
   });

   return panzoom;
}

/* ============================================================
   MAP PRESET + DATE PICKER
============================================================ */

function initMapControls(mapPreset, mapDateInput, includeOffDisplayCheckbox) {
   const fp = flatpickr(mapDateInput, {
      defaultDate: new Date(),
      dateFormat: 'Y-m-d',
      allowInput: true,
      clickOpens: true,
      minDate: 'today',
      monthSelectorType: 'static',
      onChange: (_, dateStr) => {
         if (mapPreset.value === 'specific-day') {
            updateMap('specific-day', dateStr);
         }
      },
   });

   function refetchCurrentSelection() {
      const preset = mapPreset.value;
      if (!preset) return;

      if (preset === 'specific-day') {
         const dateStr = mapDateInput.value || fp.input.value;
         if (!dateStr) return;
         updateMap('specific-day', dateStr);
      } else {
         updateMap(preset, null);
      }
   }

   mapPreset.addEventListener('change', () => {
      const preset = mapPreset.value;

      if (!preset) {
         mapDateInput.style.display = 'none';
         return;
      }

      if (preset === 'specific-day') {
         mapDateInput.style.display = 'inline-block';
         updateMap('specific-day', mapDateInput.value || fp.input.value);
      } else {
         mapDateInput.style.display = 'none';
         updateMap(preset, null);
      }
   });

   if (includeOffDisplayCheckbox) {
      includeOffDisplayCheckbox.addEventListener('change', () => {
         refetchCurrentSelection();
      });
   }

   // Fire initial fetch
   mapPreset.dispatchEvent(new Event('change'));
}

/* ============================================================
   OPTIONAL: FOCUS FROM URL (?focus=Species)
============================================================ */

function initFocusFromQuery() {
   const focus = getQueryParam('focus');
   if (!focus) return;

   const species = decodeURIComponent(focus);
   const exhibitParam = getQueryParam('exhibit');
   const exhibit = exhibitParam ? decodeURIComponent(exhibitParam) : null;

   focusAnimalFromQuery(species, exhibit);

   // Remove params so refresh doesn't re-trigger
   history.replaceState({}, '', 'map.html');
}

function focusAnimalFromQuery(speciesName, exhibitName) {
   if (!speciesName) return;

   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');

   const preset = mapPreset?.value || 'specific-day';
   const date =
      preset === 'specific-day'
         ? (mapDateInput?.value || new Date().toISOString().slice(0, 10))
         : null;

   // Fetch markers (optionally filtered) then focus
   updateMap(
      preset,
      preset === 'specific-day' ? date : null,
      { focusSpecies: speciesName, focusExhibit: exhibitName }
   );
}

/* ============================================================
   SEARCH
============================================================ */

function debounce(fn, delay = 250) {
   let t = null;
   return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
   };
}

function initAnimalSearch(inputEl) {
   if (!inputEl) return;

   const onChange = debounce(() => {
      const query = (inputEl.value || '').trim();

      // Optional: clear results when empty
      const resultsEl = document.getElementById('animalSearchResults');
      if (resultsEl && !query) {
         resultsEl.innerHTML = '';
         return;
      }

      $.ajax({
         type: 'POST',
         url: '/search-animals',
         contentType: 'application/json',
         dataType: 'json',
         data: JSON.stringify({ query }),
         success: function (response) {
            renderAnimalSearchResults(response);
         },
      });
   }, 250);

   inputEl.addEventListener('input', onChange);
}

function renderAnimalSearchResults(response) {
   const resultsEl = document.getElementById('animalSearchResults');
   if (!resultsEl) return;

   const rows = response?.results ?? response?.animals ?? response ?? [];
   resultsEl.innerHTML = '';

   if (!Array.isArray(rows) || rows.length === 0) {
      resultsEl.innerHTML = `<div class="animal-result-empty">No results.</div>`;
      return;
   }

   rows.forEach(row => {
      const species = row.SPECIES ?? row.species ?? '';
      const exhibit = row.EXHIBIT ?? row.exhibit ?? '';

      const item = document.createElement('div');
      item.className = 'animal-result';

      const left = document.createElement('div');
      left.className = 'animal-result-left';

      const speciesEl = document.createElement('div');
      speciesEl.className = 'animal-result-species';
      speciesEl.textContent = species;

      const exhibitEl = document.createElement('div');
      exhibitEl.className = 'animal-result-exhibit';
      exhibitEl.textContent = exhibit ? `Exhibit: ${exhibit}` : '';

      left.appendChild(speciesEl);
      left.appendChild(exhibitEl);

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'animal-result-map-btn';
      btn.textContent = 'View on Map';

      // ✅ NO PAGE RELOAD: focus in-place
      btn.addEventListener('click', (e) => {
         e.stopPropagation();
         focusAnimalOnMap(species, exhibit);
      });

      item.appendChild(left);
      item.appendChild(btn);

      resultsEl.appendChild(item);
   });
}

/* ============================================================
   FOCUS FROM SEARCH (NO NAVIGATION)
============================================================ */

function focusSpeciesFromSearch(speciesName) {
   if (!speciesName) return;

   // Use current preset/date and refetch markers with speciesToInclude,
   // then focusSpeciesOnMap runs in the AJAX success callback.
   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');

   const preset = mapPreset?.value || 'specific-day';

   const date =
      preset === 'specific-day'
         ? (mapDateInput?.value || new Date().toISOString().slice(0, 10))
         : null;

   if (preset === 'specific-day') {
      updateMap('specific-day', date, { focusSpecies: speciesName });
   } else {
      updateMap(preset, null, { focusSpecies: speciesName });
   }
}

/* ============================================================
   MAP UPDATE
============================================================ */

function updateMap(preset, date, options = null) {
   if (preset === 'summer') return sendAnimalRequest('Jul', 20, null, options);
   if (preset === 'winter') return sendAnimalRequest('Jan', 30, null, options);

   const month = getMonth(date);
   const day = getDay(date);

   if (isWithinNextNDays(date, 7)) {
      fetchForecastTemp(date)
         .then(temp => sendAnimalRequest(month, day, temp, options))
         .catch(() => sendAnimalRequest(month, day, null, options));
   } else {
      sendAnimalRequest(month, day, null, options);
   }
}

function fetchForecastTemp(dateStr) {
   return fetch(
      `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&units=metric&appid=${apiKey}`
   )
      .then(res => res.json())
      .then(data => {
         const dailyForecasts = data.list.filter(f => f.dt_txt.startsWith(dateStr));
         if (dailyForecasts.length === 0) return null;

         return (
            dailyForecasts.reduce((sum, f) => sum + f.main.temp, 0) /
            dailyForecasts.length
         );
      });
}

function sendAnimalRequest(month, day, temp, options = null) {
   const includeOffDisplayAnimals =
      document.querySelector('#includeOffDisplayAnimals')?.checked ?? false;

   const speciesToInclude =
      options?.focusSpecies ? [options.focusSpecies] : [];

   $.ajax({
      type: 'POST',
      url: '/get-visible-animals',
      contentType: 'application/json',
      data: JSON.stringify({
         month,
         day,
         temp,
         includeOffDisplayAnimals,
         speciesToInclude,
      }),
      success: function (response) {
         addMarkers(response.animals);

         if (options?.focusSpecies) {
            setTimeout(() => {
               focusAnimalOnMap(options.focusSpecies, options.focusExhibit || null);
            }, 0);
         }
      },
   });
}

/* ============================================================
   DATE HELPERS
============================================================ */

function isWithinNextNDays(dateStr, n) {
   const today = new Date();
   today.setHours(0, 0, 0, 0);

   const target = parseLocalDate(dateStr);
   target.setHours(0, 0, 0, 0);

   const diffDays = (target - today) / 86400000;
   return diffDays >= 0 && diffDays <= n;
}

function parseLocalDate(dateStr) {
   const [year, month, day] = dateStr.split('-').map(Number);
   return new Date(year, month - 1, day);
}

function getMonth(dateStr) {
   const date = parseLocalDate(dateStr);
   return date.toLocaleString('en-US', { month: 'short' }).toUpperCase();
}

function getDay(dateStr) {
   const date = parseLocalDate(dateStr);
   return date.getDate();
}

/* ============================================================
   MARKERS
============================================================ */

function clearMarkers() {
   const mapInner = document.getElementById('mapInner');
   if (!mapInner) return;
   mapInner.querySelectorAll('.marker').forEach(marker => marker.remove());
}

function addMarkers(animals) {
   clearMarkers();

   lastAnimals = animals || [];
   markerElsByCoord.clear();

   const mapInner = document.getElementById('mapInner');
   if (!mapInner) return;

   const markerMap = new Map();

   animals.forEach(animal => {
      const key = `${animal.x_coord}|${animal.y_coord}`;
      if (!markerMap.has(key)) {
         markerMap.set(key, { x: animal.x_coord, y: animal.y_coord, animals: [] });
      }
      markerMap.get(key).animals.push(animal);
   });

   markerMap.forEach(group => {
      const animalsOnExhibit = group.animals;
      if (animalsOnExhibit.length === 0) return;


      const el = document.createElement('div');
      el.className = 'marker';
      el.style.left = `${group.x}%`;
      el.style.top = `${group.y}%`;
      el.style.title = '';

      // ✅ custom hover tooltip text (no native tooltip)
      if (animalsOnExhibit.length === 1) {
         el.dataset.hover = animalsOnExhibit[0].species;
      } else {
         const first = animalsOnExhibit[0].species;
         el.dataset.hover = `${first} + ${animalsOnExhibit.length - 1}`;
      }
      el.removeAttribute('title'); // ensure browser tooltip doesn't show

      markerElsByCoord.set(`${group.x}|${group.y}`, el);

      // attach animals to marker so focus can find it
      el.__animals = animalsOnExhibit;

      const colour = likelihoodToColor(animalsOnExhibit[0].likelihood);
      const colourForUrl = colour.replace('#', '');

      if (animalsOnExhibit.length === 1) {
         el.style.backgroundColor = colour;
         el.style.backgroundImage = getAnimalIconUrl(
            animalsOnExhibit[0].exhibit,
            animalsOnExhibit[0].species,
            colourForUrl
         );
         el.textContent = '';
      } else {
         el.style.backgroundImage = 'none';
         el.style.backgroundColor = colour;
         el.textContent = animalsOnExhibit.length;
      }

      mapInner.appendChild(el);
      TooltipController.attachToMarker(el, animalsOnExhibit);
   });
}

function likelihoodToColor(likelihood) {
   likelihood = Math.max(0, Math.min(100, likelihood));
   const colors = [
      '#7a0000', '#9c0d00', '#be1a00', '#e03f00', '#ff6500',
      '#ff7f00', '#ff9900', '#ffb300', '#ffcc33', '#ffff33',
      '#e0ff33', '#c4ff33', '#a8ff33', '#8cff33', '#70ff33',
      '#55cc33', '#3abb33', '#2eb33a', '#259933', '#1fa544',
   ];
   const index = Math.round((likelihood / 100) * (colors.length - 1));
   return colors[index];
}

function getAnimalIconUrl(exhibit, species, backgroundColourForUrl) {
   const normalizedExhibit = normalizeParameter(exhibit);
   const normalizedAnimal = normalizeParameter(species);
   return `url("/images/animal-icons/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}-${backgroundColourForUrl}.png")`;
}

/* ============================================================
   HOVER TOOLTIP (themed)
============================================================ */

const hoverTooltip = document.getElementById('hoverTooltip');

function showHoverTooltip(text) {
   if (!hoverTooltip) return;
   hoverTooltip.textContent = text || '';
   hoverTooltip.style.display = text ? 'block' : 'none';
}

function hideHoverTooltip() {
   if (!hoverTooltip) return;
   hoverTooltip.style.display = 'none';
}

function positionHoverTooltip(clientX, clientY) {
   if (!hoverTooltip || hoverTooltip.style.display === 'none') return;

   const pad = 14;
   const offsetX = 18;
   const offsetY = 22;

   // measure after content is set
   const rect = hoverTooltip.getBoundingClientRect();

   let x = clientX + offsetX;
   let y = clientY - rect.height - offsetY;

   // if it would go off the top, place below cursor instead
   if (y < pad) y = clientY + offsetY;

   // clamp inside viewport
   x = Math.max(pad, Math.min(window.innerWidth - rect.width - pad, x));
   y = Math.max(pad, Math.min(window.innerHeight - rect.height - pad, y));

   hoverTooltip.style.left = `${x}px`;
   hoverTooltip.style.top = `${y}px`;
}

/* ============================================================
   FOCUS FLOW (NO RELOAD)
============================================================ */

function focusAnimalOnMap(speciesName, exhibitName) {
   if (!mapPanzoom || !speciesName) return;

   const target = findBestAnimalMatch(speciesName, exhibitName);
   if (!target) return;

   const { markerEl, animals } = target;

   const mapInner = document.getElementById('mapInner');
   const viewport = mapInner?.parentElement;
   if (!mapInner || !viewport) return;

   const targetScale = 3;
   mapPanzoom.zoom(targetScale, { animate: false });

   requestAnimationFrame(() => {
      centerMarkerWithContain(markerEl, viewport);

      requestAnimationFrame(() => {
         centerMarkerWithContain(markerEl, viewport);

         TooltipController.open(markerEl, animals);

         // Jump to the exact animal card (match both fields)
         setTimeout(() => jumpTooltipToAnimal(speciesName, exhibitName), 0);

         const focusedAnimal =
            animals
               .filter(a => a.species === speciesName && (!exhibitName || a.exhibit === exhibitName))
               .reduce((best, a) => (!best || Number(a.likelihood) > Number(best.likelihood) ? a : best), null)
            || animals.find(a => a.species === speciesName)
            || animals[0];

         // ✅ force marker icon to match the focused animal (not “first in marker”)
         setMarkerToSpecificAnimalIcon(markerEl, focusedAnimal);

         showOffDisplayBannerForAnimal(focusedAnimal);
      });
   });
}

function findBestAnimalMatch(speciesName, exhibitName) {
   let best = null; 
   // best = { markerEl, animals, animal, likelihood }

   for (const marker of markerElsByCoord.values()) {
      const animals = marker.__animals || [];

      for (const a of animals) {
         if (a.species !== speciesName) continue;
         if (exhibitName && a.exhibit !== exhibitName) continue;

         const l = Number(a.likelihood) || 0;

         // Choose the single best matching animal across ALL markers
         if (!best || l > best.likelihood) {
            best = { markerEl: marker, animals, animal: a, likelihood: l };
         }
      }
   }

   return best; // or null
}

function setMarkerToSpecificAnimalIcon(markerEl, animal) {
   if (!markerEl || !animal) return;

   const colour = likelihoodToColor(animal.likelihood);
   const colourForUrl = colour.replace('#', '');

   markerEl.textContent = '';
   markerEl.style.backgroundColor = colour;
   markerEl.style.backgroundImage = getAnimalIconUrl(
      animal.exhibit,
      animal.species,
      colourForUrl
   );
}

function centerMarkerWithContain(markerEl, viewportEl) {
   const vRect = viewportEl.getBoundingClientRect();
   const mRect = markerEl.getBoundingClientRect();

   const vCx = vRect.left + vRect.width / 2;
   const vCy = vRect.top + vRect.height / 2;

   const mCx = mRect.left + mRect.width / 2;
   const mCy = mRect.top + mRect.height / 2;

   const dx = vCx - mCx;
   const dy = vCy - mCy;

   const scale = mapPanzoom.getScale ? mapPanzoom.getScale() : 1;
   mapPanzoom.pan(dx / scale, dy / scale, { relative: true, animate: false });
}

function jumpTooltipToAnimal(speciesName, exhibitName) {
   const carousel = document.querySelector('.tooltip-carousel');
   if (!carousel) return;

   const cards = Array.from(carousel.children);
   if (cards.length === 0) return;

   let index = Number(carousel.dataset.index || 0);
   if (cards[index]) cards[index].style.display = 'none';

   const targetIndex = cards.findIndex(card => {
      const link = card.querySelector('.species-link');
      if (!link) return false;

      const s = link.dataset.species;
      const e = link.dataset.exhibit;
      return s === speciesName && (!exhibitName || e === exhibitName);
   });

   const newIndex = targetIndex >= 0 ? targetIndex : 0;
   cards[newIndex].style.display = 'flex';
   carousel.dataset.index = newIndex;
}

/* ============================================================
   OFF-DISPLAY BANNER
============================================================ */

let offDisplayBannerEl = null;

function ensureOffDisplayBanner() {
   if (offDisplayBannerEl) return offDisplayBannerEl;

   const el = document.createElement('div');
   el.className = 'off-display-banner';
   el.style.display = 'none';

   el.innerHTML = `
      <div class="off-display-icon">⚠</div>
      <div class="off-display-text"></div>
      <button class="off-display-close" type="button" aria-label="Close">×</button>
   `;

   el.addEventListener('click', (e) => e.stopPropagation());

   el.querySelector('.off-display-close').addEventListener('click', (e) => {
      e.stopPropagation();
      hideOffDisplayBanner();
   });

   document.body.appendChild(el);
   offDisplayBannerEl = el;
   return el;
}

function showOffDisplayBannerForAnimal(animal) {
   if (!animal.seasonally_off_display_message) return;

   const banner = ensureOffDisplayBanner();

   if (!animal || Number(animal.likelihood) !== 0) {
      hideOffDisplayBanner();
      return;
   }

   banner.querySelector('.off-display-text').innerHTML = animal.seasonally_off_display_message;

   banner.style.display = 'flex';
}

function hideOffDisplayBanner() {
   if (!offDisplayBannerEl) return;
   offDisplayBannerEl.style.display = 'none';
}

/* ============================================================
   TOOLTIP CONTROLLER
============================================================ */

const TooltipController = (() => {
   let openMarker = null;
   let animalsForOpen = [];
   let carousel = null;
   let globalListenersInstalled = false;

   function isOpen() {
      return tooltip && tooltip.style.display === 'flex';
   }

   function attachToMarker(marker, animals) {
      marker.addEventListener('click', (e) => {
         e.stopPropagation();
         toggle(marker, animals);
      });

      // ✅ themed hover tooltip
      marker.addEventListener('mouseenter', (e) => {
         showHoverTooltip(marker.dataset.hover || '');
         positionHoverTooltip(e.clientX, e.clientY);
      });

      marker.addEventListener('mousemove', (e) => {
         positionHoverTooltip(e.clientX, e.clientY);
      });

      marker.addEventListener('mouseleave', () => {
         hideHoverTooltip();
      });
   }

   function toggle(marker, animals) {
      if (isOpen() && openMarker === marker) close();
      else open(marker, animals);
   }

   function open(marker, animals) {
      if (!tooltip) return;
      if (isOpen()) close();

      openMarker = marker;
      animalsForOpen = animals || [];
      carousel = null;

      if (animalsForOpen[0]) {
         setMarkerToAnimalIcon(marker, animalsForOpen[0]);
         marker.textContent = '';
      }

      renderTooltip(animalsForOpen);

      tooltip.style.display = 'flex';
      tooltip.style.pointerEvents = 'auto';
      positionTooltip(marker);

      showOffDisplayBannerForAnimal(animalsForOpen[0] || null);
   }

   function close() {
      if (!tooltip || !isOpen()) return;

      tooltip.style.display = 'none';
      tooltip.style.pointerEvents = 'none';
      clearTooltipContent();

      if (openMarker && animalsForOpen.length > 1) {
         const colour = likelihoodToColor(animalsForOpen[0].likelihood);
         setMarkerToCount(openMarker, animalsForOpen.length, colour);
      }

      openMarker = null;
      animalsForOpen = [];
      carousel = null;

      hideOffDisplayBanner();
   }

   function renderTooltip(animals) {
      clearTooltipContent();

      const content = document.createElement('div');
      content.className = 'tooltip-content';

      carousel = createCarousel(animals);
      content.appendChild(carousel);
      tooltip.appendChild(content);

      if (animals.length > 1) {
         tooltip.classList.remove('no-arrows');
         tooltip.appendChild(createTooltipNav(carousel));
      } else {
         tooltip.classList.add('no-arrows');
      }
   }

   function createTooltipNav(carouselEl) {
      const nav = document.createElement('div');
      nav.className = 'tooltip-nav';

      const leftArrow = createArrow('<', () => carouselStep(carouselEl, -1));
      leftArrow.classList.add('tooltip-prev', 'visible');

      const rightArrow = createArrow('>', () => carouselStep(carouselEl, +1));
      rightArrow.classList.add('tooltip-next', 'visible');

      nav.appendChild(leftArrow);
      nav.appendChild(document.createElement('div'));
      nav.appendChild(rightArrow);
      return nav;
   }

   function clearTooltipContent() {
      if (!tooltip) return;
      tooltip.innerHTML = '';
   }

   function setMarkerToCount(marker, count, colour) {
      marker.textContent = count;
      marker.style.backgroundImage = 'none';
      marker.style.backgroundColor = colour;
   }

   function setMarkerToAnimalIcon(marker, animal) {
      if (!animal) return;

      const colour = likelihoodToColor(animal.likelihood);
      const colourForUrl = colour.replace('#', '');

      marker.style.backgroundColor = colour;
      marker.style.backgroundImage = getAnimalIconUrl(
         animal.exhibit,
         animal.species,
         colourForUrl
      );
   }

   function carouselStep(carouselEl, delta) {
      if (!carouselEl) return;

      const cards = Array.from(carouselEl.children);
      if (cards.length === 0) return;

      let index = Number(carouselEl.dataset.index || 0);

      cards[index].style.display = 'none';
      index = (index + delta + cards.length) % cards.length;
      cards[index].style.display = 'flex';
      carouselEl.dataset.index = index;

      if (openMarker && animalsForOpen[index]) {
         setMarkerToAnimalIcon(openMarker, animalsForOpen[index]);
         openMarker.textContent = '';
      }

      showOffDisplayBannerForAnimal(animalsForOpen[index] || null);
   }

   function initGlobalListeners() {
      if (globalListenersInstalled) return;
      globalListenersInstalled = true;

      document.addEventListener('click', (e) => {
         const link = e.target.closest('.species-link');
         if (link) {
            e.stopPropagation();

            const card = link.closest('.tooltip-card');
            let animal = null;

            if (card) {
               const idx = Number(card.dataset.index);
               if (!Number.isNaN(idx)) animal = animalsForOpen[idx] || null;
            }

            if (!animal) {
               const species = link.dataset.species;
               animal = animalsForOpen.find(a => a.species === species) || null;
            }

            if (animal) openSpeciesOverlayFromAnimal(animal);
            return;
         }

         if (!isOpen()) return;

         const clickedMarker = e.target.closest('.marker');
         const clickedTooltip = tooltip.contains(e.target);

         if (!clickedMarker && !clickedTooltip) close();
      });

      document.addEventListener('keydown', (e) => {
         if (!isOpen()) return;

         if (e.key === 'Escape') close();
         if (e.key === 'ArrowRight') carouselStep(carousel, +1);
         if (e.key === 'ArrowLeft') carouselStep(carousel, -1);
      });
   }

   return {
      attachToMarker,
      initGlobalListeners,
      open,
      close,
      toggle,
   };
})();

/* ============================================================
   CAROUSEL + TOOLTIP UI HELPERS
============================================================ */

function createCarousel(animals) {
   const carousel = document.createElement('div');
   carousel.className = 'tooltip-carousel';
   carousel.dataset.index = 0;

   animals.forEach((a, i) => {
      carousel.appendChild(createTooltipCard(a, i));
   });

   return carousel;
}

function createTooltipCard(a, index) {
   const card = document.createElement('div');
   card.className = 'tooltip-card';
   card.dataset.index = index;
   card.style.display = index === 0 ? 'flex' : 'none';

   const exhibit = normalizeParameter(a.exhibit);
   const species = normalizeParameter(a.species);

   card.innerHTML = `
      <div class="tooltip-image-frame">
         <img
            src="images/animals/${exhibit}/${species}.png"
            alt="${a.species}"
            class="tooltip-image"
         >
      </div>

      <strong class="species-link"
         data-species="${a.species}"
         data-exhibit="${a.exhibit}"
         data-enclosure="${a.enclosure_type}">
         ${a.species}
      </strong>

      <span>Exhibit: ${a.exhibit}</span>
      <span>Enclosure Type: ${a.enclosure_type}</span>
      <span>Likelihood: ${getLikelihoodPhrase(a.likelihood)} (~${a.likelihood}%)</span>
   `;
   return card;
}

function getLikelihoodPhrase(likelihood) {
   if (likelihood >= 95) return 'Very high';
   if (likelihood >= 80) return 'High';
   if (likelihood >= 60) return 'Medium';
   if (likelihood >= 40) return 'Moderate';
   if (likelihood >= 20) return 'Low';
   return 'Very low';
}

function createArrow(symbol, onClick) {
   const arrow = document.createElement('div');
   arrow.className = 'tooltip-arrow';
   arrow.textContent = symbol;
   arrow.addEventListener('click', e => {
      e.stopPropagation();
      onClick();
   });
   return arrow;
}

function positionTooltip(marker) {
   if (!tooltip) return;

   const rect = marker.getBoundingClientRect();
   const tooltipRect = tooltip.getBoundingClientRect();
   const padding = 12;

   let left = rect.left + rect.width / 2 - tooltipRect.width / 2;
   let top = rect.top - tooltipRect.height - 12;

   if (top < padding) top = rect.bottom + 12;

   left = Math.max(padding, Math.min(window.innerWidth - tooltipRect.width - padding, left));
   top = Math.max(padding, Math.min(window.innerHeight - tooltipRect.height - padding, top));

   tooltip.style.left = `${left}px`;
   tooltip.style.top = `${top}px`;
}

/* ============================================================
   SPECIES OVERLAY (unchanged)
============================================================ */

const speciesOverlay = document.getElementById('speciesOverlay');
let speciesOverlayContent = null;

if (speciesOverlay) {
   speciesOverlayContent = speciesOverlay.querySelector('.species-overlay-content');

   speciesOverlay.addEventListener('click', e => {
      if (e.target === speciesOverlay) closeSpeciesOverlay();
   });
}

function openSpeciesOverlayFromAnimal(animal) {
   if (!speciesOverlay || !speciesOverlayContent || !animal) return;

   const contentHTML = buildSpeciesContentHTML(animal);

   speciesOverlayContent.innerHTML =
      buildOverlayHeaderHTML() +
      buildOverlayScrollHTML(contentHTML);

   speciesOverlayContent
      .querySelector('.species-close')
      .addEventListener('click', closeSpeciesOverlay);

   speciesOverlay.classList.remove('hidden');
}

function buildOverlayHeaderHTML() {
   return `
      <div class="species-overlay-header">
         <button class="species-close" type="button" aria-label="Close">×</button>
      </div>
   `;
}

function buildOverlayScrollHTML(innerHTML) {
   return `
      <div class="species-overlay-scroll">
         ${innerHTML}
      </div>
   `;
}

function buildSpeciesContentHTML(animal) {
   const section = (title, value) => {
      if (!value || !value.trim()) return '';
      return `
         <div class="section">
            <strong>${title}:</strong>
            <p>${value}</p>
         </div>
      `;
   };

   return `
      <img
         src="images/animals/${normalizeParameter(animal.exhibit)}/${normalizeParameter(animal.species)}.png"
         class="new-animal-image"
      >

      <h2 class="animal-species-name">${animal.species}</h2>
      ${animal.latin_name ? `<h6 class="latin-name">${animal.latin_name}</h6>` : ''}
      <h4 class="animal-exhibit">${animal.exhibit}</h4>

      ${section('Seasonal Viewing Summary', animal.seasonal_viewing_summary)}
      ${section('Seasonal Viewing Information', animal.seasonal_viewing_information)}
      ${section('General Viewing Tips', animal.general_viewing_tips)}
      ${section('Seasonal Viewing Tips', animal.seasonal_viewing_tips)}
      ${section('Identification', animal.identification)}
      ${section('Habitat And Range', animal.habitat_and_range)}
      ${section('Diet And Feeding', animal.diet_and_feeding)}
      ${section('Behaviour And Life Cycle', animal.behaviour_and_life_cycle)}
      ${section('Adaptations', animal.adaptations)}
      ${section('Reproduction And Life Cycle', animal.reproduction_and_life_cycle)}
      ${section('Animals At The Zoo', animal.animals_at_the_zoo)}
   `;
}

function closeSpeciesOverlay() {
   if (!speciesOverlay) return;
   speciesOverlay.classList.add('hidden');
}

/* ============================================================
   animals.html bits
============================================================ */

function displayRegions() {
   const regions = [
      { name: 'Africa', hasExhibits: true },
      { name: 'Americas', hasExhibits: true },
      { name: 'Australasia', hasExhibits: true },
      { name: 'Canadian Domain', hasExhibits: false },
      { name: 'Discovery Zone', hasExhibits: true },
      { name: 'Eurasia Wilds', hasExhibits: false },
      { name: 'Indo-Malaya', hasExhibits: true },
      { name: 'Tundra Trek', hasExhibits: false },
   ];

   const list = document.querySelector('.list');
   list.innerHTML = '';

   regions.forEach(({ name, hasExhibits }) => {
      const btn = document.createElement('button');
      btn.classList.add('list-button');

      const fileName = normalizeParameter(name);

      const img = document.createElement('img');
      img.src = `images/regions/${fileName}.png`;
      img.classList.add('list-image');

      btn.appendChild(img);
      btn.appendChild(document.createTextNode(name));

      btn.addEventListener('click', () => {
         if (hasExhibits) {
            displayExhibits(name);
         } else {
            displayAnimals(name, name);
         }
      });

      list.appendChild(btn);
   });
}

function displayExhibits(region) {
   $.ajax({
      type: 'POST',
      url: '/get-exhibits-in-region',
      contentType: 'application/json',
      data: JSON.stringify({ region }),
      success: function (response) {
         const list = document.querySelector('.list');

         list.innerHTML = '';

         const backBtn = document.createElement('button');
         backBtn.classList.add('list-button', 'back-button');
         backBtn.textContent = 'Back';

         backBtn.addEventListener('click', () => {
            displayRegions();
         });

         list.appendChild(backBtn);

         response.exhibits.forEach(exhibit => {
            const btn = document.createElement('button');
            btn.classList.add('list-button');

            const fileName = normalizeParameter(exhibit);

            const img = document.createElement('img');
            img.src = `images/exhibits/${fileName}.png`;
            img.classList.add('list-image');

            btn.appendChild(img);
            btn.appendChild(document.createTextNode(exhibit));

            btn.addEventListener('click', () => {
               displayAnimals(region, exhibit);
            });

            list.appendChild(btn);
         });
      },
   });
}

function displayAnimals(region, exhibit) {
   $.ajax({
      type: 'POST',
      url: '/get-animals-in-exhibit',
      contentType: 'application/json',
      data: JSON.stringify({ exhibit }),
      success: function (response) {
         const list = document.querySelector('.list');
         list.innerHTML = '';

         const backBtn = document.createElement('button');
         backBtn.classList.add('list-button', 'back-button');
         backBtn.textContent = 'Back';

         backBtn.addEventListener('click', () => {
            if (region == exhibit) displayRegions();
            else displayExhibits(region);
         });

         list.appendChild(backBtn);

         response.animals.forEach(animalName => {
            const btn = document.createElement('button');
            btn.classList.add('list-button');

            const normalizedExhibit = normalizeParameter(exhibit);
            const normalizedAnimal = normalizeParameter(animalName);

            const img = document.createElement('img');
            img.src = `images/animal-icons/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}.png`;
            img.classList.add('list-image');

            btn.appendChild(img);
            btn.appendChild(document.createTextNode(animalName));

            btn.addEventListener('click', () => {
               displayAnimalInformation(region, exhibit, animalName);
            });

            list.appendChild(btn);
         });
      },
   });
}

function displayAnimalInformation(region, exhibit, animal) {
   $.ajax({
      type: 'POST',
      url: '/get-animal-information',
      contentType: 'application/json',
      dataType: 'json',
      data: JSON.stringify({ species: animal }),
      success: function (response) {
         const animal_info = response.information[0];
         if (!animal_info) return;

         const list = document.querySelector('.list');

         list.innerHTML =
            buildAnimalInfoBackButtonHTML() +
            buildSpeciesContentHTML(animal_info);

         list.scrollTop = 0;

         list.querySelector('.animal-info-back-button')
            .addEventListener('click', () => {
               displayAnimals(region, exhibit);
            });

         const exhibitHeading = list.querySelector('.animal-exhibit');

         if (exhibitHeading) {
            const viewBtn = document.createElement('button');
            viewBtn.className = 'view-on-map-button';
            viewBtn.textContent = 'View on Map';
            viewBtn.type = 'button';

            viewBtn.addEventListener('click', () => {
               const species = encodeURIComponent(animal);
               const ex = encodeURIComponent(exhibit);
               window.location.href = `map.html?focus=${species}&exhibit=${ex}`;
            });

            exhibitHeading.insertAdjacentElement('afterend', viewBtn);
         }
      },
   });
}

function buildAnimalInfoBackButtonHTML() {
   return `
      <button class="animal-info-back-button" type="button">
         ← Back
      </button>
   `;
}

function normalizeParameter(parameter) {
   return parameter.toLowerCase().replaceAll(' ', '-').replaceAll("'", '');
}