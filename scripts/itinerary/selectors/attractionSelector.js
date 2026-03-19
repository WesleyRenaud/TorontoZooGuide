import { normalizeParameter } from '../../utils/normalize.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
import { showItineraryConfirmPopup } from '../panel/components/confirmPopup.js';

const STORAGE_KEY = 'tzg.itineraryAttractions';

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
      if ([ 'true', 't', 'yes', 'y', '1' ].includes(s)) return true;
      if ([ 'false', 'f', 'no', 'n', '0' ].includes(s)) return false;
   }

   return false;
}

function isSeasonalAttraction(row) {
   const v =
      row.part_of_seasonal_attraction ??
      row.PART_OF_SEASONAL_ATTRACTION ??
      row.part_of_seasonal_exhibit ??
      row.PART_OF_SEASONAL_EXHIBIT ??
      row.is_seasonal ??
      row.IS_SEASONAL ??
      row.seasonal ??
      row.SEASONAL ??
      false;

   if (v === true) return true;
   if (v === false) return false;

   if (typeof v === 'number') return v !== 0;

   if (typeof v === 'string') {
      const s = v.trim().toLowerCase();
      if ([ 'true', 't', 'yes', 'y', '1' ].includes(s)) return true;
      if ([ 'false', 'f', 'no', 'n', '0' ].includes(s)) return false;
   }

   return false;
}

function isClosed(row) {
   const v =
      row.is_closed ??
      row.IS_CLOSED ??
      row.closed ??
      row.CLOSED ??
      false;

   if (v === true) return true;
   if (v === false) return false;

   if (typeof v === 'number') return v !== 0;

   if (typeof v === 'string') {
      const s = v.trim().toLowerCase();
      if ([ 'true', 't', 'yes', 'y', '1' ].includes(s)) return true;
      if ([ 'false', 'f', 'no', 'n', '0' ].includes(s)) return false;
   }

   return false;
}

function getSubtitle(row) {
   return isFreeWithAdmission(row) ? 'Free With Admission' : 'Extra Charge';
}

function buildAttractionImageSrc(row) {
   const name = getAttractionName(row);
   const nameFile = normalizeParameter(name || '');
   if (!nameFile) return null;
   return `../images/attractions/${nameFile}.png`;
}

function migrateIfNeeded(arr) {
   if (!Array.isArray(arr)) return [];

   return arr
      .map(x => {
         if (typeof x === 'string') {
            const name = x;
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

         if (x && typeof x === 'object') {
            const name = x.name ?? x.NAME ?? x.title ?? x.TITLE ?? '';
            const id = x.id ?? name;

            return {
               id,
               name,
               subtitle: x.subtitle ?? '',
               freeWithAdmission:
                  x.freeWithAdmission ??
                  x.free_with_admission ??
                  x.is_free_with_admission ??
                  false,
               seasonal:
                  x.seasonal ??
                  x.isSeasonal ??
                  x.is_seasonal ??
                  x.part_of_seasonal_attraction ??
                  x.part_of_seasonal_exhibit ??
                  false,
               isClosed:
                  x.isClosed ??
                  x.is_closed ??
                  x.closed ??
                  false,
               infoLink: x.infoLink ?? x.info_link ?? x.link ?? x.LINK ?? null,
               imageSrc: x.imageSrc ?? x.image_src ?? x.image ?? null,
            };
         }

         return null;
      })
      .filter(Boolean)
      .filter(x => x.id);
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

      buildSearchPayload: (query) => ({
         query,
         includeAttractions: true,
         includeClosedAttractions,
      }),

      extractRows: (response) =>
         (Array.isArray(response?.attractions) ? response.attractions :
          Array.isArray(response) ? response :
          Array.isArray(response?.results) ? response.results :
          []),

      getId: (row) => getAttractionName(row),
      getTitle: (row) => getAttractionName(row) || 'Attraction',
      getSubtitle: (row) => getSubtitle(row),
      getImageSrc: (row) => buildAttractionImageSrc(row),
      getInfoLink: (row) => getInfoLink(row),

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
         text.textContent = 'Include seasonal attractions';

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