// scripts/itinerary/wildEncounterSelector.js
import { normalizeParameter } from '../utils/normalize.js';
import { createItinerarySelectorController } from './selectors/createSelectorController.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';
const DATE_STORAGE_KEY = 'tzg.itineraryDateISO';

/* -------------------------------------------------- */
/* DATE HELPERS                                       */
/* -------------------------------------------------- */

function getSavedISODate() {
   return localStorage.getItem(DATE_STORAGE_KEY) || '';
}

// Monday=1 ... Sunday=7
function isoDateToMonFirstDow(iso) {
   const d = iso ? new Date(`${iso}T12:00:00`) : new Date();
   const js = d.getDay();
   return js === 0 ? 7 : js;
}

/* -------------------------------------------------- */
/* ROW FIELD HELPERS                                  */
/* -------------------------------------------------- */

function getName(row) {
   return row.name ?? row.NAME ?? '';
}

function getMeetingSpot(row) {
   return (
      row.meeting_spot ??
      row.MEETING_SPOT ??
      row.meetingSpot ??
      row.MEETINGSPOT ??
      row.location ??
      row.LOCATION ??
      ''
   );
}

function getTimeOfDay(row) {
   return row.time_of_day ?? row.TIME_OF_DAY ?? row.time ?? row.TIME ?? '';
}

function getLink(row) {
   const v = row.link ?? row.LINK ?? row.info_link ?? row.INFO_LINK ?? null;
   const s = typeof v === 'string' ? v.trim() : '';
   return s ? s : null;
}

/* -------------------------------------------------- */
/* KEY + IMAGE                                        */
/* -------------------------------------------------- */

function buildKey(row, dayOfWeek) {
   const name = getName(row);
   const spot = getMeetingSpot(row);
   const time = getTimeOfDay(row);
   return `${name}||${spot}||${dayOfWeek}||${time}`;
}

function buildWildEncounterImageSrc(name) {
   const file = normalizeParameter(name || '');
   if (!file) return null;
   return `../images/wild-encounters/${file}.png`;
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
               meetingSpot: x.meetingSpot ?? x.meeting_spot ?? '',
               dayOfWeek: x.dayOfWeek ?? '',
               timeOfDay: x.timeOfDay ?? x.time_of_day ?? '',
               link: x.link ?? null,
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

export function createItineraryWildEncounterSelectorController({
   mountEl,
   onPrev,
   onFinish,
} = {}) {
   let dayOfWeek = 1;

   function computeDayOfWeek() {
      const iso = getSavedISODate();
      dayOfWeek = isoDateToMonFirstDow(iso);
      return dayOfWeek;
   }

   function makeSelection(row) {
      const name = getName(row);
      const meetingSpot = getMeetingSpot(row);
      const timeOfDay = getTimeOfDay(row);
      const link = getLink(row);

      const key = buildKey(row, dayOfWeek);

      return {
         id: key,
         key,
         name,
         meetingSpot,
         dayOfWeek,
         timeOfDay,
         link,
         imageSrc: buildWildEncounterImageSrc(name),
      };
   }

   return createItinerarySelectorController({
      mountEl,

      // Wild Encounters step only has Prev + Finish in your UI
      onPrev,
      onFinish,
      hideNextButton: true,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateIfNeeded,

      /* ----------------------------- */
      /* SEARCH CONFIG                 */
      /* ----------------------------- */

      buildSearchPayload: (query) => ({
         query,
         dayOfWeek: computeDayOfWeek(),
         includeWildEncounters: true,
      }),

      extractRows: (response) =>
         Array.isArray(response?.wild_encounters) ? response.wild_encounters : [],

      /* ----------------------------- */
      /* ROW ID / DISPLAY              */
      /* ----------------------------- */

      getId: (row) => buildKey(row, dayOfWeek),

      getTitle: (row) => getName(row) || 'Wild Encounter',

      getSubtitle: (row) => {
         const spot = getMeetingSpot(row);
         const time = getTimeOfDay(row);

         return `${spot ? `Meeting Spot: ${spot}` : 'Meeting Spot: —'}${
            time ? `  •  Time: ${time}` : ''
         }`;
      },

      getImageSrc: (row) => buildWildEncounterImageSrc(getName(row)),

      // Optional "More Info" link under the subtitle
      getInfoLink: (row) => getLink(row),

      makeSelection,

      /* ----------------------------- */
      /* UI TEXT                       */
      /* ----------------------------- */

      topTitle: 'Itinerary Builder',
      h1: 'Wild Encounters',
      subtitle: 'Search and add wild encounters to your plan.',
      emptyText: 'No wild encounters found for this day',
   });
}