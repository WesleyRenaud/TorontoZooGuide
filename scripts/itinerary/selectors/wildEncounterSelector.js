import { normalizeParameter } from '../../utils/normalize.js';
import { createItinerarySelectorController } from './createSelectorController.js';
import { getItineraryDateSearchContext } from '../itinerarySearchContext.js';

const STORAGE_KEY = 'tzg.itineraryWildEncounters';

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

function buildWildEncounterImageSrc(name) {
   const file = normalizeParameter(name || '');
   if (!file) return null;
   return `../images/wild-encounters/${file}.png`;
}

function migrateIfNeeded(arr) {
   if (!Array.isArray(arr)) return [];

   return arr
      .map(x => {
         if (typeof x === 'string') {
            return {
               id: x,
               name: x,
               meetingSpot: '',
               timeOfDay: '',
               link: null,
               imageSrc: buildWildEncounterImageSrc(x),
            };
         }

         if (x && typeof x === 'object') {
            const name = x.name ?? x.NAME ?? '';
            const id = x.id ?? name;

            return {
               id,
               name,
               meetingSpot: x.meetingSpot ?? x.meeting_spot ?? x.MEETING_SPOT ?? '',
               timeOfDay: x.timeOfDay ?? x.time_of_day ?? x.TIME_OF_DAY ?? '',
               link: x.link ?? x.LINK ?? x.info_link ?? x.INFO_LINK ?? null,
               imageSrc: x.imageSrc ?? x.image_src ?? x.image ?? buildWildEncounterImageSrc(name),
            };
         }

         return null;
      })
      .filter(Boolean)
      .filter(x => x.id);
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

      extractRows: response =>
         Array.isArray(response?.wildEncounters)
            ? response.wildEncounters
            : Array.isArray(response?.wild_encounters)
            ? response.wild_encounters
            : [],

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