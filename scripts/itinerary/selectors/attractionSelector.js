import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import {
   normalizeStoredBoolean,
   normalizeStoredLink,
   normalizeStoredString,
} from './base/storedSelection.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';

const STORAGE_KEY = 'tzg.itineraryAttractions';

function getAttractionName(row) {
   return row.name ?? '';
}

function getInfoLink(row) {
   const v = row.info_link ?? null;
   const s = typeof v === 'string' ? v.trim() : '';
   return s ? s : null;
}

function isFreeWithAdmission(row) {
   return row.free_with_admission === true;
}

function isSeasonalAttraction(row) {
   return row.part_of_seasonal_attraction === true;
}

function isClosed(row) {
   return row.is_closed === true;
}

function getSubtitle(row) {
   return isFreeWithAdmission(row) ? 'Free With Admission' : 'Extra Charge';
}

function buildAttractionImageSrc(row) {
   const name = getAttractionName(row);
   const nameFile = normalizeAssetKey(name || '');
   if (!nameFile) return null;
   return `../images/attractions/${nameFile}.png`;
}

function migrateIfNeeded(arr) {
   if (!Array.isArray(arr)) return [];

   return arr
      .map((item) => {
         if (typeof item === 'string') {
            const name = item.trim();

            if (!name) {
               return null;
            }

            return {
               id: name,
               name,
               subtitle: '',
               freeWithAdmission: false,
               seasonal: false,
               infoLink: null,
               imageSrc: null,
            };
         }

         if (item && typeof item === 'object') {
            const name = normalizeStoredString(item.name);
            const id = normalizeStoredString(item.id) || name;

            if (!id) {
               return null;
            }

            return {
               id,
               name,
               subtitle: normalizeStoredString(item.subtitle),
               freeWithAdmission: normalizeStoredBoolean(item.freeWithAdmission),
               seasonal: normalizeStoredBoolean(item.seasonal),
               isClosed: normalizeStoredBoolean(item.isClosed),
               infoLink: normalizeStoredLink(item.infoLink),
               imageSrc: normalizeStoredLink(item.imageSrc),
            };
         }

         return null;
      })
      .filter(Boolean)
}

function makeSelection(row) {
   const name = getAttractionName(row);
   const freeWithAdmission = isFreeWithAdmission(row);
   const seasonal = isSeasonalAttraction(row);
   const isClosedValue = isClosed(row);
   const subtitle = getSubtitle(row);
   const infoLink = getInfoLink(row);
   const imageSrc = buildAttractionImageSrc(row);

   return {
      id: name,
      name,
      subtitle,
      freeWithAdmission,
      seasonal,
      isClosed: isClosedValue,
      infoLink,
      imageSrc,
   };
}

export function createItineraryAttractionSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
} = {}) {
   let includeClosedAttractions = false;

   return createItinerarySelectorController({
      mountEl,
      onNext,
      onPrev,
      onFinish,
      onClose,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateIfNeeded,

      getContext: () => getItineraryDateSearchContext({ includeTemp: false }),

      buildSearchPayload: query => ({
         query,
         includeAttractions: true,
         includeClosedAttractions,
      }),

      extractRows: response => response.attractions,

      getId: row => getAttractionName(row),
      getTitle: row => getAttractionName(row) || 'Attraction',
      getSubtitle: row => getSubtitle(row),
      getImageSrc: row => buildAttractionImageSrc(row),
      getInfoLink: row => getInfoLink(row),

      makeSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Add Attractions',
      subtitle: 'Search and add attractions to your plan.',
      emptyText: 'No attractions found.',

      onBeforeToggleAdd: ({ row, isSelected, proceed }) => {
         if (isSelected) {
            proceed();
            return;
         }

         if (!includeClosedAttractions) {
            proceed();
            return;
         }

         if (!isClosed(row)) {
            proceed();
            return;
         }

         const name = getAttractionName(row) || 'This attraction';

         showItineraryConfirmPopup({
            title: 'Attraction May Be Closed',
            message: `The ${name} is closed on your visit date. Do you still want to add it to your itinerary?`,
            confirmText: 'Add',
            cancelText: 'Cancel',
            onConfirm: proceed,
         });
      },

      renderExtraControls: ({ bodyEl, rerunSearch }) => {
         includeClosedAttractions = false;

         const toggleWrap = document.createElement('div');
         toggleWrap.className = 'itin-selector-toggle-wrap';

         const label = document.createElement('label');
         label.className = 'toggle-row itin-selector-toggle-row';

         const checkbox = document.createElement('input');
         checkbox.type = 'checkbox';
         checkbox.checked = false;

         const text = document.createElement('span');
         text.textContent = 'Include closed attractions';

         checkbox.addEventListener('change', () => {
            includeClosedAttractions = checkbox.checked;
            rerunSearch?.();
         });

         label.appendChild(checkbox);
         label.appendChild(text);
         toggleWrap.appendChild(label);

         bodyEl.insertBefore(toggleWrap, bodyEl.querySelector('.itin-search-input'));
      },
   });
}
