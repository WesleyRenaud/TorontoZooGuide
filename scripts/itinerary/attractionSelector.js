// scripts/itinerary/attractionSelector.js
import { normalizeParameter } from '../utils/normalize.js';
import { createItinerarySelectorController } from './selectors/createSelectorController.js';

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
      if (['true', 't', 'yes', 'y', '1'].includes(s)) return true;
      if (['false', 'f', 'no', 'n', '0'].includes(s)) return false;
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
   const subtitle = getSubtitle(row);
   const infoLink = getInfoLink(row);
   const imageSrc = buildAttractionImageSrc(row);

   return {
      id: name,
      name,
      subtitle,
      freeWithAdmission,
      infoLink,
      imageSrc,
   };
}

export function createItineraryAttractionSelectorController({ mountEl, onNext, onPrev, onFinish } = {}) {
   return createItinerarySelectorController({
      mountEl,
      onNext,
      onPrev,
      onFinish,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateIfNeeded,

      buildSearchPayload: (query) => ({ query, includeAttractions: true }),
      extractRows: (response) =>
         (Array.isArray(response?.attractions) ? response.attractions :
          Array.isArray(response) ? response :
          Array.isArray(response?.results) ? response.results :
          []),

      getId: (row) => getAttractionName(row),
      getTitle: (row) => getAttractionName(row) || 'Attraction',
      getSubtitle: (row) => getSubtitle(row),
      getImageSrc: (row) => buildAttractionImageSrc(row),
      getInfoLink: (row) => getInfoLink(row), // ✅ controller renders the link

      makeSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Add Attractions',
      subtitle: 'Search and add attractions to your plan.',
      emptyText: 'No attractions found.',
   });
}