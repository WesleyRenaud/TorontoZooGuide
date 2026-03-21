import { normalizeParameter } from '../../utils/normalize.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';

const STORAGE_KEY = 'tzg.itineraryGuardiansTalks';

function getName(row) {
   return row.name ?? row.NAME ?? '';
}

function getLocation(row) {
   return row.location ?? row.LOCATION ?? '';
}

function getTimeOfDay(row) {
   return row.time_of_day ?? row.TIME_OF_DAY ?? '';
}

function buildTalkImageSrc(name) {
   const file = normalizeParameter(name || '');
   if (!file) return null;

   return `../images/guardians-talks/${file}.png`;
}

function migrateIfNeeded(arr) {
   if (!Array.isArray(arr)) return [];

   return arr
      .map(x => {
         if (typeof x === 'string') {
            return {
               id: x,
               name: x,
               location: '',
               timeOfDay: '',
               imageSrc: buildTalkImageSrc(x),
            };
         }

         if (x && typeof x === 'object') {
            const name = x.name ?? x.NAME ?? '';
            const id = x.id ?? name;

            return {
               id,
               name,
               location: x.location ?? x.LOCATION ?? '',
               timeOfDay: x.timeOfDay ?? x.time_of_day ?? x.TIME_OF_DAY ?? '',
               imageSrc: x.imageSrc ?? x.image_src ?? x.image ?? buildTalkImageSrc(name),
            };
         }

         return null;
      })
      .filter(Boolean)
      .filter(x => x.id);
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

      extractRows: response =>
         Array.isArray(response?.guardiansTalks)
            ? response.guardiansTalks
            : Array.isArray(response?.guardians_talks)
            ? response.guardians_talks
            : [],

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