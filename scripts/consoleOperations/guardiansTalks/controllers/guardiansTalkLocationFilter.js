import {
   getGuardiansTalkLocations,
   getGuardiansTalkNamesAtLocation,
} from '../../../api/consoleOperationsApi.js';
import {
   populateGuardiansTalkDropdown,
   populateValueDropdown,
} from '../../options/dropdowns.js';
import { APP_STRINGS } from '../../../strings.js';

export function createGuardiansTalkLocationFilterController({
   locationEl,
   talkNameEl,
} = {}) {
   function getFieldValue(fieldEl) {
      return fieldEl?.value.trim() ?? '';
   }

   function getLocationName(location) {
      return typeof location === 'string'
         ? location.trim()
         : String(location?.location ?? location?.name ?? '').trim();
   }

   function populateLocationDropdown(locations) {
      const locationNames = (locations ?? [])
         .map(getLocationName)
         .filter(Boolean)
         .sort((a, b) => a.localeCompare(b));

      populateValueDropdown(
         locationEl,
         locationNames,
         APP_STRINGS.placeholders.location
      );
   }

   function clearTalkDropdown() {
      if (talkNameEl?.tagName === 'SELECT') {
         populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if (talkNameEl) {
         talkNameEl.value = '';
      }
   }

   async function refreshLocations() {
      if (locationEl?.tagName !== 'SELECT') {
         return;
      }

      try {
         const result = await getGuardiansTalkLocations();
         const guardiansTalkLocations = result?.guardians_talk_locations ?? [];
         populateLocationDropdown(guardiansTalkLocations);
      }
      catch(err) {
      }
   }

   async function refreshTalks() {
      const location = getFieldValue(locationEl);

      clearTalkDropdown();

      if (!location) {
         return;
      }

      try {
         const result = await getGuardiansTalkNamesAtLocation({
            location
         });

         const guardiansTalks = result?.guardians_talks ?? [];

         if (talkNameEl?.tagName === 'SELECT') {
            populateGuardiansTalkDropdown(talkNameEl, guardiansTalks);
         }
      }
      catch(err) {
      }
   }

   locationEl?.addEventListener('change', () => {
      if (talkNameEl) {
         talkNameEl.value = '';
      }

      refreshTalks();
   });

   return {
      refreshLocations,
      refresh: refreshTalks,
      clear() {
         clearTalkDropdown();
      }
   };
}
