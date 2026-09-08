import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { Strings } from '../../../strings.js';

export class GuardiansTalkLocationFilter {
   static createGuardiansTalkLocationFilterController({
      locationEl,
      talkNameEl,
   } = {}) {

      function getLocationName(location) {
         return typeof location === 'string'
            ? ValueNormalizer.asTrimmedString(location)
            : ValueNormalizer.asTrimmedString(location?.location ?? location?.name);
      }

      function populateLocationDropdown(locations) {
         const locationNames = (locations ?? [])
            .map(getLocationName)
            .filter(Boolean)
            .sort((a, b) => a.localeCompare(b));

         ConsoleDropdownPopulator.populateValueDropdown(
            locationEl,
            locationNames,
            Strings.placeholders.location
         );
      }

      function clearTalkDropdown() {
         if (talkNameEl?.tagName === 'SELECT') {
            ConsoleDropdownPopulator.populateGuardiansTalkDropdown(talkNameEl, []);
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
            const result = await ConsoleOperationsClient.getGuardiansTalkLocations();
            const guardiansTalkLocations = result?.guardians_talk_locations ?? [];
            populateLocationDropdown(guardiansTalkLocations);
         }
         catch(err) {
         }
      }

      async function refreshTalks() {
         const location = ControllerHelper.getFieldValue(locationEl);

         clearTalkDropdown();

         if (!location) {
            return;
         }

         try {
            const result = await ConsoleOperationsClient.getGuardiansTalkNamesAtLocation({
               location
            });

            const guardiansTalks = result?.guardians_talks ?? [];

            if (talkNameEl?.tagName === 'SELECT') {
               ConsoleDropdownPopulator.populateGuardiansTalkDropdown(talkNameEl, guardiansTalks);
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
