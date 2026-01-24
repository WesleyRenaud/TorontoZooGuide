const apiKey = '657afbbbe68b892616c765dce8e68d6b';
const lat = 43.8177;   // Toronto Zoo latitude
const lon = -79.1859;

// Ensure the DOM is loaded before running
document.addEventListener('DOMContentLoaded', () => {
   const mapInner = document.getElementById('mapInner');

   if (mapInner != null) {
      const panzoom = Panzoom(mapInner, {
      maxScale: 3,
      minScale: 1,
      contain: 'outside'
      });

      mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

      // Optional: enable wheel zoom
      mapInner.parentElement.addEventListener('wheel', panzoom.zoomWithWheel);

      // Get all region labels
      const regionLabels = document.querySelectorAll('.region-label');
      const exhibitLabels = document.querySelectorAll('.exhibit-label');

      // Threshold zoom scale for hiding labels
      const regionHideZoomScale = 1.5;  // labels disappear when zoom > 1.5
      const exhibitHideZoomScale = 2; // labels disappear when zoom > 2

      // Listen to Panzoom events
      mapInner.addEventListener('panzoomchange', () => {
         const currentScale = panzoom.getScale();

         // Remove the region/exhibit labels independently
         regionLabels.forEach(label => {
            if (currentScale > regionHideZoomScale) {
                  label.style.display = 'none';
            } else {
                  label.style.display = 'block';
            }
         });

         exhibitLabels.forEach(label => {
            if (currentScale > exhibitHideZoomScale) {
                  label.style.display = 'none';
            } else {
                  label.style.display = 'block';
            }
         });
      });
   }

   const mapPreset = document.getElementById('mapPreset');
   const mapDateInput = document.getElementById('mapDate');

   // Initialize Flatpickr
   const fp = flatpickr(mapDateInput, {
      defaultDate: new Date(),
      dateFormat: 'Y-m-d',
      allowInput: true,
      clickOpens: true,
      minDate: 'today',
      monthSelectorType: "static",
      onChange: function (_, dateStr) {
         if (mapPreset.value === 'specific-day') {
            updateMap('specific-day', dateStr);
         }
      }
   });

   // Handle preset changes
   mapPreset.addEventListener('change', () => {
      const preset = mapPreset.value;

      // No selection (placeholder)
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

   // Initialize visibility on page load
   mapPreset.dispatchEvent(new Event('change'));
});

function updateMap(preset, date) {
   let month = null;
   let day = null;
   let temp = null;

   // Presets
   if (preset === 'summer') {
      month = 'Jul';
      day = 20;
      sendAnimalRequest(month, day, null);
      return;
   }

   if (preset === 'winter') {
      month = 'Jan';
      day = 30;
      sendAnimalRequest(month, day, null);
      return;
   }

   // Specific day
   month = getMonth(date);
   day = getDay(date);

   // If within forecast range, fetch temperature
   if (isWithinNextNDays(date, 7)) {
      fetch(`https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&units=metric&appid=${apiKey}`)
         .then(res => res.json())
         .then(data => {
            const targetDateStr = date;

            const dailyForecasts = data.list.filter(f =>
               f.dt_txt.startsWith(targetDateStr)
            );

            if (dailyForecasts.length > 0) {
               // IMPORTANT: use average, not max
               temp =
                  dailyForecasts.reduce((sum, f) => sum + f.main.temp, 0) /
                  dailyForecasts.length;
            }

            sendAnimalRequest(month, day, temp);
         });
   }
   else {
      // Outside forecast range → backend average model
      sendAnimalRequest(month, day, null);
   }
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

      el.style.backgroundColor = likelihoodToColor(animalsOnExhibit[0].likelihood);

      mapInner.appendChild(el);

      // Attach click-to-open tooltip with all species at this exhibit
      attachTooltip(el, animalsOnExhibit);
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

/* ============================================================
   TOOLTIP FUNCTIONS
============================================================ */

// Attach click behavior to show/hide tooltip
let openTooltipMarker = null;
function attachTooltip(marker, animals) {
   marker.addEventListener('click', (e) => {
      e.stopPropagation(); // prevent map click events

      const isVisible = tooltip.style.display === 'flex';
      // If the tooltip is visible and this marker is the open one, toggle (close it)
      if (isVisible && openTooltipMarker === marker) {
         hideTooltip();
         openTooltipMarker = null;
      } else {
         hideTooltip(); // Close any open tooltip first
         showTooltipForMarker(marker, animals);
         openTooltipMarker = marker;
      }
   });
}

let lastAnimals = [];

function showTooltipForMarker(marker, animals) {
   lastAnimals = animals;

   clearTooltip();
   tooltip.style.display = 'flex';
   tooltip.style.pointerEvents = 'auto';

   const content = document.createElement('div');
   content.className = 'tooltip-content';

   const carousel = createCarousel(animals);
   carousel._marker = marker;
   currentCarousel = carousel;

   // Enable arrow key navigation
   enableTooltipKeyboard(carousel);

   content.appendChild(carousel);
   tooltip.appendChild(content);

   // Only create arrow nav if multiple cards
   if (animals.length > 1) {
      const nav = document.createElement('div');
      nav.className = 'tooltip-nav';

      const leftArrow = createArrow('<', () => carouselPrev(carousel));
      leftArrow.classList.add('tooltip-prev', 'visible');

      const rightArrow = createArrow('>', () => carouselNext(carousel));
      rightArrow.classList.add('tooltip-next', 'visible');

      nav.appendChild(leftArrow);
      nav.appendChild(document.createElement('div')); // spacer
      nav.appendChild(rightArrow);

      tooltip.appendChild(nav);
      tooltip.classList.remove('no-arrows');
   } else {
      // Single species - remove arrow spacing
      tooltip.classList.add('no-arrows');
   }

   positionTooltip(marker);
}

// Hide tooltip completely
function hideTooltip() {
   tooltip.style.display = 'none';
   openTooltipMarker = null;
}

// Clear the tooltip content
function clearTooltip() {
   tooltip.innerHTML = '';
   currentCarousel = null;
}

/* ============================================================
   CAROUSEL FUNCTIONS
============================================================ */

function createCarousel(animals) {
   const carousel = document.createElement('div');
   carousel.className = 'tooltip-carousel';
   animals.forEach((a, i) => {
      const card = document.createElement('div');
      card.className = 'tooltip-card';
      card.dataset.index = i;

      card.innerHTML = `
         <div class="tooltip-image-frame">
            <img 
               src="images/animals/${a.exhibit}/${a.species.replaceAll(' ', '-')}.png"
               alt="${a.species}"
               class="tooltip-image"
            >
         </div>

         <strong class="species-link" data-species="${a.species}" data-exhibit="${a.exhibit}" data-exhibit="${a.exhibit_type}">
            ${a.species}
         </strong>
         <span>Exhibit: ${a.exhibit}</span>
         <span>Exhibit: ${a.exhibit_type}</span>
         <span>Likelihood: ${getLikelihoodPhrase(a.likelihood)} (~${a.likelihood}%)</span>
      `;

      card.style.display = i === 0 ? 'flex' : 'none';
      carousel.appendChild(card);
   });
   carousel.dataset.index = 0;
   return carousel;
}

function getLikelihoodPhrase(likelihood) {
   if (likelihood >= 95) { // 95%
      return 'Very high';
   }
   else if (likelihood >= 80) {
      return 'High';
   }
   else if (likelihood >= 60) {
      return 'Medium';
   }
   else if (likelihood >= 40) {
      return 'Moderate';
   }
   else if (likelihood >= 20) {
      return 'Low';
   }
   else {
      return 'Very low';
   }
}

function carouselNext(carousel) {
   const cards = Array.from(carousel.children);
   let index = Number(carousel.dataset.index);
   cards[index].style.display = 'none';
   index = (index + 1) % cards.length;
   cards[index].style.display = 'flex';
   carousel.dataset.index = index;
   if (carousel._marker) {
      carousel._marker.style.backgroundColor =
         likelihoodToColor(lastAnimals[index].likelihood);
   }
}

function carouselPrev(carousel) {
   const cards = Array.from(carousel.children);
   let index = Number(carousel.dataset.index);
   cards[index].style.display = 'none';
   index = (index - 1 + cards.length) % cards.length;
   cards[index].style.display = 'flex';
   carousel.dataset.index = index;
   if (carousel._marker) {
      carousel._marker.style.backgroundColor =
         likelihoodToColor(lastAnimals[index].likelihood);
   }
}

// Add keyboard navigation for carousel
function enableTooltipKeyboard(carousel) {
   function handleKey(e) {
      if (e.key === "ArrowRight") {
         carouselNext(carousel);
      } else if (e.key === "ArrowLeft") {
         carouselPrev(carousel);
      }
   }

   document.addEventListener('keydown', handleKey);

   // Remove listener when tooltip is hidden
   tooltip.addEventListener('mouseleave', () => {
      document.removeEventListener('keydown', handleKey);
   }, { once: true });
}

/* ============================================================
   ARROWS
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

function updateArrowVisibility(count, left, right) {
   if (count > 1) {
      left.classList.add('visible');
      right.classList.add('visible');
   } else {
      left.classList.remove('visible');
      right.classList.remove('visible');
   }
}

/* ============================================================
   POSITIONING
============================================================ */

function positionTooltip(marker) {
   const rect = marker.getBoundingClientRect();
   const tooltipRect = tooltip.getBoundingClientRect();

   const padding = 12; // distance from screen edges

   // Desired position (centered above marker)
   let left = rect.left + rect.width / 2 - tooltipRect.width / 2;
   let top  = rect.top - tooltipRect.height - 12;

   // If it would go off the top, place it below instead
   if (top < padding) {
      top = rect.bottom + 12;
   }

   // Clamp horizontally inside viewport
   left = Math.max(padding, left);
   left = Math.min(window.innerWidth - tooltipRect.width - padding, left);

   // Clamp vertically just in case
   top = Math.max(padding, top);
   top = Math.min(window.innerHeight - tooltipRect.height - padding, top);

   tooltip.style.left = `${left}px`;
   tooltip.style.top = `${top}px`;
}

/* ============================================================
   CLOSE TOOLTIP ON OUTSIDE CLICK
============================================================ */

document.addEventListener('click', (e) => {
   // For opening an animal card
   const link = e.target.closest('.species-link');
   if (!link) return;

   e.stopPropagation();

   const species = link.dataset.species;
   openSpeciesOverlay(species);

   // For closing an animl card
   if (!tooltip.contains(e.target)) {
      hideTooltip();
   }
});

// Global click listener
document.addEventListener('click', (e) => {
   // If the click is on a marker or inside the tooltip, do nothing
   if (tooltip.contains(e.target) || e.target.closest('.marker')) {
      return;
   }

   // Otherwise, hide the tooltip
   if (tooltip.style.display === 'flex') {
      hideTooltip();
   }
});

document.addEventListener('keydown', e => {
   // Close tooltip on Escape
   if (e.key === 'Escape' && tooltip.style.display === 'flex') {
      hideTooltip();
   }
});

/* ============================================================
   SPECIES OVERLAY CONTENT
============================================================ */

const speciesOverlay = document.getElementById('speciesOverlay');
const speciesOverlayContent = speciesOverlay.querySelector('.species-overlay-content');

function openSpeciesOverlay(species) {
   const animal = getAnimalBySpecies(species);
   if (!animal) return;

   const section = (title, value) => {
      if (!value || !value.trim()) return '';
      return `
         <div class="section">
            <strong>${title}:</strong>
            <p>${value}</p>
         </div>
      `;
   };

   speciesOverlayContent.innerHTML = `
      <div class="species-overlay-header">
         <button class="species-close">×</button>
      </div>

      <div class="species-overlay-scroll">
         <img
            src="images/animals/${animal.exhibit}/${animal.species.replaceAll(' ', '-')}.png"
            class="new-animal-image"
         >

         <h2>${animal.species}</h2>

         ${section('exhibit', animal.exhibit)}
         ${section('Seasonal Viewing Summary', animal.seasonal_viewing_summary)}
         ${section('Seasonal Viewing Tips', animal.seasonal_viewing_tips)}
         ${section('General Viewing Tips', animal.general_viewing_tips)}
         ${section('Animal Info', animal.animal_info)}
         ${section('Specific Animal Information', animal.specific_animal_info)}
      </div>
   `;

   speciesOverlayContent
      .querySelector('.species-close')
      .addEventListener('click', closeSpeciesOverlay);

   speciesOverlay.classList.remove('hidden');
}

speciesOverlay.addEventListener('click', e => {
   if (e.target === speciesOverlay) closeSpeciesOverlay();
});

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
