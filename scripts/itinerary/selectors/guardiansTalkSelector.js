// scripts/itinerary/guardiansTalkSelector.js
import { normalizeParameter } from '../../utils/normalize.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';
const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';
const DATE_STORAGE_KEY = 'tzg.itineraryDateISO';

/* -------------------------------------------------- */
/* DATE HELPERS                                       */
/* -------------------------------------------------- */

// Monday=1 ... Sunday=7
function isoDateToMonFirstDow(iso) {
   const d = iso ? new Date(`${iso}T12:00:00`) : new Date();
   if (!Number.isFinite(d.getTime())) return 1;

   const js = d.getDay();
   return js === 0 ? 7 : js;
}

function getSavedISODate() {
   return localStorage.getItem(DATE_STORAGE_KEY) || '';
}

/* -------------------------------------------------- */
/* BACKEND FIELD HELPERS                              */
/* -------------------------------------------------- */

function getName(row) {
   return row.name ?? row.NAME ?? '';
}

function getLocation(row) {
   return row.location ?? row.LOCATION ?? '';
}

function getTimeOfDay(row) {
   return row.time_of_day ?? row.TIME_OF_DAY ?? '';
}

/* -------------------------------------------------- */
/* KEY GENERATION                                     */
/* -------------------------------------------------- */

function buildKey(row, dayOfWeek) {
   const name = getName(row);
   const loc = getLocation(row);
   const time = getTimeOfDay(row);

   return `${name}||${loc}||${dayOfWeek}||${time}`;
}

/* -------------------------------------------------- */
/* IMAGE                                              */
/* -------------------------------------------------- */

function buildTalkImageSrc(name) {
   const file = normalizeParameter(name || '');
   if (!file) return null;

   return `../images/meet-the-guardians-talks/${file}.png`;
}

/* -------------------------------------------------- */
/* STORAGE MIGRATION                                  */
/* -------------------------------------------------- */

function migrateIfNeeded(arr) {
   if (!Array.isArray(arr)) return [];

   return arr
      .map(x => {
         if (typeof x === 'string') return null;

         if (x && typeof x === 'object') {
            const key = x.key ?? '';
            return {
               id: key,
               key,
               name: x.name ?? '',
               location: x.location ?? '',
               timeOfDay: x.timeOfDay ?? '',
               dayOfWeek: x.dayOfWeek ?? '',
               imageSrc: x.imageSrc ?? null,
            };
         }

         return null;
      })
      .filter(Boolean)
      .filter(x => x.id);
}

/* -------------------------------------------------- */
/* FACTORY WRAPPER                                    */
/* -------------------------------------------------- */

export function createItineraryGuardiansTalkSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
} = {}) {
   let dayOfWeek = 1;

   function getDayOfWeekContext() {
      const iso = getSavedISODate();
      dayOfWeek = isoDateToMonFirstDow(iso);
      return { dayOfWeek };
   }

   function makeSelection(row) {
      const name = getName(row);
      const location = getLocation(row);
      const timeOfDay = getTimeOfDay(row);

      const key = buildKey(row, dayOfWeek);

      return {
         id: key,
         key,
         name,
         location,
         timeOfDay,
         dayOfWeek,
         imageSrc: buildTalkImageSrc(name),
      };
   }

   return createItinerarySelectorController({
      mountEl,
      onPrev,
      onNext,
      onFinish,
      onClose,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateIfNeeded,

      // ✅ put date-derived context here
      getContext: getItineraryDateSearchContext,

      buildSearchPayload: (query) => ({
         query,
         includeMeetTheGuardiansTalks: true,
      }),

      extractRows: (response) =>
         Array.isArray(response?.meet_the_guardians_talks)
            ? response.meet_the_guardians_talks
            : [],

      getId: (row) => buildKey(row, dayOfWeek),

      getTitle: (row) =>
         getName(row) || 'Talk',

      getSubtitle: (row) => {
         const loc = getLocation(row);
         const time = getTimeOfDay(row);

         return `${loc ? `Location: ${loc}` : 'Location: —'}${time ? `  •  Time: ${time}` : ''}`;
      },

      getImageSrc: (row) =>
         buildTalkImageSrc(getName(row)),

      makeSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Meet the Guardians',
      subtitle: 'Search and add talks to your plan.',
      emptyText: 'No Meet the Guardians talks found for this day',
   });
}