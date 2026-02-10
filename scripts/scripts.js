const apiKey = '657afbbbe68b892616c765dce8e68d6b';
const lat = 43.8177;
const lon = -79.1859;

function getPageName() {
   return window.location.pathname.split('/').pop().replace('.html', '');
}

document.addEventListener('DOMContentLoaded', () => {
   if (getPageName() !== 'map') return;
   initMapPage();
});

function initMapPage() {
   TooltipController.initGlobalListeners();

   const mapInner = document.getElementById('mapInner');
   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');

   if (!mapInner || !mapPreset || !mapDateInput) return;

   initPanzoom(mapInner);
   initMapControls(mapPreset, mapDateInput);
}

function initPanzoom(mapInner) {
   const panzoom = Panzoom(mapInner, {
      maxScale: 10,
      minScale: 1,
      contain: 'outside',
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

function initMapControls(mapPreset, mapDateInput) {
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

   mapPreset.dispatchEvent(new Event('change'));
}

/* ============================================================
   MAP UPDATE
============================================================ */

function updateMap(preset, date) {
   if (preset === 'summer') return sendAnimalRequest('Jul', 20, null);
   if (preset === 'winter') return sendAnimalRequest('Jan', 30, null);

   const month = getMonth(date);
   const day = getDay(date);

   if (isWithinNextNDays(date, 7)) {
      fetchForecastTemp(date)
         .then(temp => sendAnimalRequest(month, day, temp))
         .catch(() => sendAnimalRequest(month, day, null));
   } else {
      sendAnimalRequest(month, day, null);
   }
}

function fetchForecastTemp(dateStr) {
   return fetch(
      `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&units=metric&appid=${apiKey}`
   )
      .then(res => res.json())
      .then(data => {
         const dailyForecasts = data.list.filter(f =>
            f.dt_txt.startsWith(dateStr)
         );

         if (dailyForecasts.length === 0) return null;

         return (
            dailyForecasts.reduce((sum, f) => sum + f.main.temp, 0) /
            dailyForecasts.length
         );
      });
}

function sendAnimalRequest(month, day, temp) {
   $.ajax({
      type: 'POST',
      url: '/get-visible-animals',
      contentType: 'application/json',
      data: JSON.stringify({ month, day, temp }),
      success: function (response) {
         addMarkers(response.animals);
      }
   });
}

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
   return new Date(year, month - 1, day); // LOCAL time
}

function getMonth(dateStr) {
   const date = parseLocalDate(dateStr);
   return date
      .toLocaleString('en-US', { month: 'short' })
      .toUpperCase();
}

function getDay(dateStr) {
   const date = parseLocalDate(dateStr);
   return date.getDate();
}

/* ============================================================
   MARKERS & TOOLTIP SYSTEM (Click-to-Open)
============================================================ */

const tooltip = document.getElementById('tooltip');
let currentCarousel = null;

// Clear all markers from the map
function clearMarkers() {
   const mapInner = document.getElementById('mapInner');
   mapInner.querySelectorAll('.marker').forEach(marker => marker.remove());
}

// Add markers to the map based on animal data
function addMarkers(animals) {
   clearMarkers();

   const mapInner = document.getElementById('mapInner');

   // Group animals by coordinate key "x|y"
   const markerMap = new Map();

   animals.forEach(animal => {
      const x = animal.x_coord;
      const y = animal.y_coord;

      const key = `${x}|${y}`;

      if (!markerMap.has(key)) {
         markerMap.set(key, {
            x,
            y,
            animals: []
         });
      }

      markerMap.get(key).animals.push(animal);
   });

   // Create one marker per coordinate
   markerMap.forEach(group => {
      const animalsOnExhibit = group.animals;

      if (animalsOnExhibit.length === 0) return;

      const el = document.createElement('div');
      el.className = 'marker';
      el.style.left = `${group.x}%`;
      el.style.top = `${group.y}%`;
      el.title = ''; // remove default browser tooltip

      const backgroundColour = likelihoodToColor(animalsOnExhibit[0].likelihood).replace('#', '');
      if (animalsOnExhibit.length === 1) {
         el.style.backgroundImage = getAnimalIconUrl(animalsOnExhibit[0].exhibit, animalsOnExhibit[0].species, backgroundColour);
      }
      else {
         el.style.backgroundColor = backgroundColour;
         el.textContent = animalsOnExhibit.length;
      }

      mapInner.appendChild(el);

      // Attach click-to-open tooltip with all species at this exhibit
      TooltipController.attachToMarker(el, animalsOnExhibit);
   });
}

function likelihoodToColor(likelihood) {
   // Clamp the likelihood to [0, 100]
   likelihood = Math.max(0, Math.min(100, likelihood));

   // 20-color palette, last color kept as #32b03a, greens adjusted to flow smoothly
   const colors = [
      '#7a0000', '#9c0d00', '#be1a00', '#e03f00', '#ff6500', // reds → oranges
      '#ff7f00', '#ff9900', '#ffb300', '#ffcc33', '#ffff33', // oranges → yellow
      '#e0ff33', '#c4ff33', '#a8ff33', '#8cff33', '#70ff33', // yellow → light green
      '#55cc33', '#3abb33', '#2eb33a', '#259933', '#1fa544'  // greens adjusted → darker towards end
   ];

   // Map 0-100 value to palette index
   const index = Math.round((likelihood / 100) * (colors.length - 1));

   return colors[index];
}

function getAnimalIconUrl(exhibit, species, backgroundColour) {
   const normalizedExhibit = normalizeParameter(exhibit);
   const normalizedAnimal = normalizeParameter(species);

   return `url("/images/animal-icons/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}-${backgroundColour}.png")`;
}

/* ============================================================
   TOOLTIP MODULE (single source of truth)
============================================================ */

const TooltipController = (() => {
   let openMarker = null;
   let animalsForOpen = [];
   let carousel = null;

   function isOpen() {
      return tooltip.style.display === 'flex';
   }

   function attachToMarker(marker, animals) {
      marker.addEventListener('click', (e) => {
         e.stopPropagation();
         toggle(marker, animals);
      });
   }

   function toggle(marker, animals) {
      if (isOpen() && openMarker === marker) {
         close();
      } else {
         open(marker, animals);
      }
   }

   function open(marker, animals) {
      // close anything already open
      if (isOpen()) close();

      openMarker = marker;
      animalsForOpen = animals;

      // when opening, show icon for first animal (and clear count text)
      setMarkerToAnimalIcon(marker, animals[0]);
      marker.textContent = '';

      renderTooltip(marker, animals);
      tooltip.style.display = 'flex';
      tooltip.style.pointerEvents = 'auto';
      positionTooltip(marker);
   }

   function close() {
      if (!isOpen()) return;

      tooltip.style.display = 'none';
      tooltip.style.pointerEvents = 'none';
      clearTooltipContent();

      // restore marker to count style
      if (openMarker && animalsForOpen.length > 1) {
         setMarkerToCount(openMarker, animalsForOpen.length);
      }

      openMarker = null;
      animalsForOpen = [];
      carousel = null;
   }

   function renderTooltip(marker, animals) {
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
      nav.appendChild(document.createElement('div')); // spacer
      nav.appendChild(rightArrow);
      return nav;
   }

   function clearTooltipContent() {
      tooltip.innerHTML = '';
   }

   function setMarkerToCount(marker, count) {
      marker.textContent = count;
      marker.style.backgroundImage = '';
      // keep marker backgroundColor as whatever you already set for clusters
   }

   function setMarkerToAnimalIcon(marker, animal) {
      if (!animal) return;
      const backgroundColour = likelihoodToColor(animal.likelihood).replace('#', '');
      marker.style.backgroundImage = getAnimalIconUrl(animal.exhibit, animal.species, backgroundColour);
   }

   // step carousel + update marker icon to match the active card
   function carouselStep(carouselEl, delta) {
      const cards = Array.from(carouselEl.children);
      let index = Number(carouselEl.dataset.index || 0);

      cards[index].style.display = 'none';
      index = (index + delta + cards.length) % cards.length;
      cards[index].style.display = 'flex';

      carouselEl.dataset.index = index;

      // keep marker icon synced with active animal
      if (openMarker && animalsForOpen[index]) {
         setMarkerToAnimalIcon(openMarker, animalsForOpen[index]);
         openMarker.textContent = '';
      }
   }

   // global listeners (called once)
   let tooltipGlobalListenersInstalled = false;

   function initGlobalListeners() {
      if (tooltipGlobalListenersInstalled) return;
      tooltipGlobalListenersInstalled = true;

      document.addEventListener('click', (e) => {
         // 1) Species link click (open overlay)
         const link = e.target.closest('.species-link');
         if (link) {
            e.stopPropagation();
            openSpeciesOverlay(link.dataset.species);
            return;
         }

         // 2) Outside click closes tooltip
         if (!isOpen()) return;

         const clickedMarker = e.target.closest('.marker');
         const clickedTooltip = tooltip.contains(e.target);

         if (!clickedMarker && !clickedTooltip) close();
      });

      document.addEventListener('keydown', (e) => {
         if (!isOpen()) return;

         if (e.key === 'Escape') {
            close();
            return;
         }

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
   CAROUSEL (smaller/cleaner)
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

/* ============================================================
   ARROWS (unchanged)
============================================================ */

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

/* ============================================================
   POSITIONING (unchanged)
============================================================ */

function positionTooltip(marker) {
   const rect = marker.getBoundingClientRect();
   const tooltipRect = tooltip.getBoundingClientRect();
   const padding = 12;

   let left = rect.left + rect.width / 2 - tooltipRect.width / 2;
   let top  = rect.top - tooltipRect.height - 12;

   if (top < padding) top = rect.bottom + 12;

   left = Math.max(padding, Math.min(window.innerWidth - tooltipRect.width - padding, left));
   top  = Math.max(padding, Math.min(window.innerHeight - tooltipRect.height - padding, top));

   tooltip.style.left = `${left}px`;
   tooltip.style.top = `${top}px`;
}

/* ============================================================
   SPECIES OVERLAY CONTENT
============================================================ */

const speciesOverlay = document.getElementById('speciesOverlay');
let speciesOverlayContent = null;

if (speciesOverlay != null) {
   speciesOverlayContent = speciesOverlay.querySelector('.species-overlay-content');
}

function openSpeciesOverlay(species) {
   const animal = getAnimalBySpecies(species);
   if (!animal) return;

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

      <h2>${animal.species}</h2>
      ${animal.latin_name ? `<h6 class="latin-name">${animal.latin_name}</h6>` : ''}
      <h4>${animal.exhibit}</h4>

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

if (speciesOverlay != null) {
   speciesOverlay.addEventListener('click', e => {
      if (e.target === speciesOverlay) closeSpeciesOverlay();
   });
}

function closeSpeciesOverlay() {
   speciesOverlay.classList.add('hidden');
}

/* ============================================================
   HELPERS/PLACEHOLDERS
============================================================ */

function getAnimalBySpecies(species) {
   if (!currentCarousel) return null;

   const cards = currentCarousel.querySelectorAll('.tooltip-card');
   for (const card of cards) {
      if (card.querySelector('.species-link')?.dataset.species === species) {
         const index = card.dataset.index;
         return lastAnimals[index];
      }
   }
   return null;
}

/* ============================================================
   animals.html
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
         // If there are no exhibits, go straight to animals for the region.
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

            const fileName = normalizeParameter(exhibit.toLowerCase);

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
      }
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
            if (region == exhibit) {
               displayRegions();
            }
            else {
               displayExhibits(region);
            }
         });

         list.appendChild(backBtn);

         response.animals.forEach(animal => {
            const btn = document.createElement('button');
            btn.classList.add('list-button');

            const normalizedExhibit = normalizeParameter(exhibit);
            const normalizedAnimal =normalizeParameter(animal);

            const img = document.createElement('img');
            img.src = `images/animal-icons/${normalizedExhibit}/${normalizedAnimal}/${normalizedAnimal}.png`;
            img.classList.add('list-image');

            btn.appendChild(img);
            btn.appendChild(document.createTextNode(animal));

            btn.addEventListener('click', () => {
               displayAnimalInformation(region, exhibit, animal);
            });

            list.appendChild(btn);
         });
      }
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

         // ✅ Reset scroll so the back button is visible
         list.scrollTop = 0;

         // Wire the back button behavior
         list.querySelector('.animal-info-back-button')
         .addEventListener('click', () => {
            displayAnimals(region, exhibit);
         });
      }
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
