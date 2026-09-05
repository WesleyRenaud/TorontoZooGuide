import { ConsoleOperationsApi } from '../../../api/consoleOperationsApi.js';
import { ControllerUtils } from '../../helpers/controllerUtils.js';
import { Dropdowns } from '../../options/dropdowns.js';
import { APP_STRINGS } from '../../../strings.js';

export class GuardiansTalkLocationFilter {
   static createGuardiansTalkLocationFilterController({
      locationEl,
      talkNameEl,
   } = {}) {

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

         Dropdowns.populateValueDropdown(
            locationEl,
            locationNames,
            APP_STRINGS.placeholders.location
         );
      }

      function clearTalkDropdown() {
         if (talkNameEl?.tagName === 'SELECT') {
            Dropdowns.populateGuardiansTalkDropdown(talkNameEl, []);
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
            const result = await ConsoleOperationsApi.getGuardiansTalkLocations();
            const guardiansTalkLocations = result?.guardians_talk_locations ?? [];
            populateLocationDropdown(guardiansTalkLocations);
         }
         catch(err) {
         }
      }

      async function refreshTalks() {
         const location = ControllerUtils.getFieldValue(locationEl);

         clearTalkDropdown();

         if (!location) {
            return;
         }

         try {
            const result = await ConsoleOperationsApi.getGuardiansTalkNamesAtLocation({
               location
            });

            const guardiansTalks = result?.guardians_talks ?? [];

            if (talkNameEl?.tagName === 'SELECT') {
               Dropdowns.populateGuardiansTalkDropdown(talkNameEl, guardiansTalks);
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
}
