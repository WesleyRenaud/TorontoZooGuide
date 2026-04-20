import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import {
   normalizeStoredLink,
   normalizeStoredString,
} from './base/storedSelection.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';

function getName(row) {
   return row.name ?? '';
}

function getMeetingSpot(row) {
   return row.meeting_spot ?? '';
}

function getTimeOfDay(row) {
   return row.time_of_day ?? '';
}

function getLink(row) {
   const v = row.link ?? null;
   const s = typeof v === 'string' ? v.trim() : '';
   return s ? s : null;
}

function buildWildEncounterImageSrc(name) {
   const file = normalizeAssetKey(name || '');
   if (!file) return null;
   return `../images/wild-encounters/${file}.png`;
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
               meetingSpot: '',
               timeOfDay: '',
               link: null,
               imageSrc: buildWildEncounterImageSrc(name),
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
               meetingSpot: normalizeStoredString(item.meetingSpot),
               timeOfDay: normalizeStoredString(item.timeOfDay),
               link: normalizeStoredLink(item.link),
               imageSrc: normalizeStoredString(item.imageSrc) || buildWildEncounterImageSrc(name),
            };
         }

         return null;
      })
      .filter(Boolean)
}

export function createItineraryWildEncounterSelectorController({
   mountEl,
   onPrev,
   onFinish,
   onClose,
} = {}) {
   function makeSelection(row) {
      const name = getName(row);
      const meetingSpot = getMeetingSpot(row);
      const timeOfDay = getTimeOfDay(row);
      const link = getLink(row);

      return {
         id: name,
         name,
         meetingSpot,
         timeOfDay,
         link,
         imageSrc: buildWildEncounterImageSrc(name),
      };
   }

   return createItinerarySelectorController({
      mountEl,

      onPrev,
      onFinish,
      onClose,
      hideNextButton: true,

      storageKey: STORAGE_KEY,
      migrateSelected: migrateIfNeeded,

      getContext: getItineraryDateSearchContext,

      buildSearchPayload: query => ({
         query,
         includeWildEncounters: true,
      }),

      extractRows: response => response.wild_encounters,

      getId: row => getName(row),

      getTitle: row => getName(row) || 'Wild Encounter',

      getSubtitle: row => {
         const spot = getMeetingSpot(row);
         const time = getTimeOfDay(row);

         return `${spot ? `Meeting Spot: ${spot}` : 'Meeting Spot: —'}${time ? `  •  Time: ${time}` : ''}`;
      },

      getImageSrc: row => buildWildEncounterImageSrc(getName(row)),

      getInfoLink: row => getLink(row),

      makeSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Wild Encounters',
      subtitle: 'Search and add wild encounters to your plan.',
      emptyText: 'No wild encounters found for this day',
   });
}
