import { normalizeAssetKey } from '../../assets/normalizeAssetKey.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { normalizeStoredString } from './base/storedSelection.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';

function getName(row) {
   return row.name ?? '';
}

function getLocation(row) {
   return row.location ?? '';
}

function getTimeOfDay(row) {
   return row.time_of_day ?? '';
}

function buildTalkImageSrc(name) {
   const file = normalizeAssetKey(name || '');
   if (!file) return null;

   return `../images/guardians-talks/${file}.png`;
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
               location: '',
               timeOfDay: '',
               imageSrc: buildTalkImageSrc(name),
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
               location: normalizeStoredString(item.location),
               timeOfDay: normalizeStoredString(item.timeOfDay),
               imageSrc: normalizeStoredString(item.imageSrc) || buildTalkImageSrc(name),
            };
         }

         return null;
      })
      .filter(Boolean)
}

export function createItineraryGuardiansTalkSelectorController({
   mountEl,
   onNext,
   onPrev,
   onFinish,
   onClose,
} = {}) {
   function makeSelection(row) {
      const name = getName(row);
      const location = getLocation(row);
      const timeOfDay = getTimeOfDay(row);

      return {
         id: name,
         name,
         location,
         timeOfDay,
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

      getContext: getItineraryDateSearchContext,

      buildSearchPayload: query => ({
         query,
         includeGuardiansTalks: true,
      }),

      extractRows: response => response.guardians_talks,

      getId: row => getName(row),

      getTitle: row =>
         getName(row) || 'Talk',

      getSubtitle: row => {
         const loc = getLocation(row);
         const time = getTimeOfDay(row);

         return `${loc ? `Location: ${loc}` : 'Location: —'}${time ? `  •  Time: ${time}` : ''}`;
      },

      getImageSrc: row =>
         buildTalkImageSrc(getName(row)),

      makeSelection,

      topTitle: 'Itinerary Builder',
      h1: 'Meet the Guardians',
      subtitle: 'Search and add talks to your plan.',
      emptyText: 'No Meet the Guardians talks found for this day',
   });
}
