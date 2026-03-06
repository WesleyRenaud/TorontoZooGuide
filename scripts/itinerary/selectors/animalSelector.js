// scripts/itinerary/animalSelector.js
import { normalizeParameter } from '../../utils/normalize.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';

const STORAGE_KEY = 'tzg.itineraryAnimals';
const OFF_DISPLAY_WARNING_THRESHOLD = 80;

function getSpecies(row) {
   return row.SPECIES ?? row.species ?? '';
}

function getExhibit(row) {
   return row.EXHIBIT ?? row.exhibit ?? '';
}

function getLikelihood(row) {
   const value = row.likelihood ?? row.LIKELIHOOD ?? null;
   const num = Number(value);
   return Number.isFinite(num) ? num : null;
}


function getLikelihoodLevel(row) {
   const likelihood = getLikelihood(row);

   if (likelihood === null) return null;
   if (likelihood < 40) return 'low';
   if (likelihood < 80) return 'medium';

   return null;
}

function isLikelyOffDisplay(row, threshold = OFF_DISPLAY_WARNING_THRESHOLD) {
   const likelihood = getLikelihood(row);
   return likelihood !== null && likelihood < threshold;
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

function migrateIfNeeded(arr) {
   if (!Array.isArray(arr)) return [];

   if (arr.length > 0 && typeof arr[0] === 'string') {
      return arr
         .filter(Boolean)
         .map(species => ({ id: species, species, exhibit: '', imageSrc: null }));
   }

   return arr
      .filter(x => x && typeof x === 'object')
      .map(x => ({
         id: x.id ?? x.species ?? x.SPECIES ?? '',
         species: x.species ?? x.SPECIES ?? '',
         exhibit: x.exhibit ?? x.EXHIBIT ?? '',
         imageSrc: x.imageSrc ?? x.image_src ?? x.image ?? null,
      }))
      .filter(x => x.id);
}

function makeSelection(row) {
   const species = getSpecies(row);
   const exhibit = getExhibit(row);
   const imageSrc = buildAnimalImageSrc(row);
   return { id: species, species, exhibit, imageSrc };
}

export function createItineraryAnimalSelectorController({ mountEl, onNext, onPrev, onFinish } = {}) {
   let includeOffDisplayAnimals = false;

   function renderAnimalRowLeft(row) {
      const species = getSpecies(row) || 'Animal';
      const subtitle = getSubtitle(row);
      const imageSrc = buildAnimalImageSrc(row);

      const content = document.createElement('div');
      content.className = 'itin-animal-content';

      const thumbWrap = document.createElement('div');
      thumbWrap.className = 'itin-animal-thumb';

      if (imageSrc) {
         const img = document.createElement('img');
         img.className = 'itin-animal-thumb-img';
         img.loading = 'lazy';
         img.alt = species ? `${species} photo` : 'Animal photo';
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

      const titleWrap = document.createElement('div');
      titleWrap.className = 'itin-animal-title-wrap';

      const titleEl = document.createElement('div');
      titleEl.className = 'animal-result-species';
      titleEl.textContent = species;

      titleWrap.appendChild(titleEl);

      const level = getLikelihoodLevel(row);

      if (level) {
         const warn = document.createElement('span');
         warn.className = `itin-likelihood-warning ${level}`;

         warn.innerHTML = `
         <svg viewBox="0 0 24 24" class="itin-warning-icon">
            <path d="M12 2L1 21h22L12 2z"></path>
            <rect x="11" y="9" width="2" height="6" fill="black"></rect>
            <circle cx="12" cy="18" r="1.6" fill="black"></circle>
         </svg>
         `;
         warn.title =
            level === 'low'
               ? 'Very low chance of seeing this animal'
               : 'This animal may be off display';

         titleWrap.appendChild(warn);
      }

      left.appendChild(titleWrap);

      if (subtitle) {
         const subtitleEl = document.createElement('div');
         subtitleEl.className = 'animal-result-exhibit';
         subtitleEl.textContent = subtitle;
         left.appendChild(subtitleEl);
      }

      content.appendChild(thumbWrap);
      content.appendChild(left);

      return content;
   }

   const controller = createItinerarySelectorController({
      mountEl,
      onNext,
      onPrev,
      onFinish,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateIfNeeded,

      getContext: getItineraryDateSearchContext,

      buildSearchPayload: (query) => ({
         query,
         includeAnimals: true,
         includeOffDisplayAnimals,
      }),

      extractRows: (response) =>
         (Array.isArray(response?.animals) ? response.animals :
          Array.isArray(response) ? response :
          response?.results) || [],

      getId: (row) => getSpecies(row),
      getTitle: (row) => getSpecies(row) || 'Animal',
      getSubtitle: (row) => getSubtitle(row),
      getImageSrc: (row) => buildAnimalImageSrc(row),

      makeSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Add Animals',
      subtitle: 'Search and add animals to your plan.',
      emptyText: 'No animals found.',

      renderRowLeft: renderAnimalRowLeft,

      onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
         if (isSelected) {
            proceed();
            return;
         }

         if (!includeOffDisplayAnimals) {
            proceed();
            return;
         }

         if (!isLikelyOffDisplay(row)) {
            proceed();
            return;
         }

         const species = getSpecies(row) || 'This animal';
         const likelihood = getLikelihood(row);

         showItineraryConfirmPopup({
            title: 'Animal May Be Off Display',
            message: likelihood === null
               ? `The ${species} may be off display on your visit date. Do you still want to add it to your itinerary?`
               : `The ${species} has a viewing likelihood below ${OFF_DISPLAY_WARNING_THRESHOLD}% (${likelihood}%) for your visit date and may be off display. Do you still want to add it to your itinerary?`,
            confirmText: 'Add',
            cancelText: 'Cancel',
            onConfirm: proceed,
         });
      },

      renderExtraControls: ({ bodyEl, rerunSearch }) => {
         includeOffDisplayAnimals = false;

         const toggleWrap = document.createElement('div');
         toggleWrap.className = 'itin-selector-toggle-wrap';

         const label = document.createElement('label');
         label.className = 'toggle-row itin-selector-toggle-row';

         const checkbox = document.createElement('input');
         checkbox.type = 'checkbox';
         checkbox.checked = false;

         const text = document.createElement('span');
         text.textContent = 'Include off-display animals';

         checkbox.addEventListener('change', () => {
            includeOffDisplayAnimals = checkbox.checked;
            rerunSearch?.();
         });

         label.appendChild(checkbox);
         label.appendChild(text);
         toggleWrap.appendChild(label);

         bodyEl.insertBefore(toggleWrap, bodyEl.querySelector('.itin-search-input'));
      },
   });

   return controller;
}