import { ConsoleOperationsClient } from '../../../api/consoleOperationsClient.js';
import { ValueNormalizer } from '../../../api/valueNormalizer.js';
import { ControllerHelper } from '../../helpers/controllerHelper.js';
import { GuardiansTalkDropdownResetHelper } from '../helpers/guardiansTalkDropdownResetHelper.js';
import { GuardiansTalkEnclosureDropdown } from '../helpers/guardiansTalkEnclosureDropdown.js';
import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';
import { Strings } from '../../../strings.js';

export class GuardiansTalkLocationFilter {
   static createGuardiansTalkLocationFilterController({
      locationEl,
      talkNameEl,
      enclosureEl,
      loadLocations = ConsoleOperationsClient.getGuardiansTalkLocations,
      loadTalks = ConsoleOperationsClient.getGuardiansTalkNamesAtLocation,
   } = {}) {
      let talksAtLocation = [];

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

      function refreshEnclosureOptions() {
         const talkName = ControllerHelper.getFieldValue(talkNameEl);
         const talk = talksAtLocation.find(item => item.name === talkName);

         GuardiansTalkEnclosureDropdown.populate(
            enclosureEl,
            talk ? talk.enclosure_names : []
         );
      }

      function clearTalkDropdown() {
         talksAtLocation = [];
         GuardiansTalkDropdownResetHelper.resetTalkDropdown({ talkNameEl });
         GuardiansTalkEnclosureDropdown.reset(enclosureEl);
      }

      async function refreshLocations() {
         if (locationEl?.tagName !== 'SELECT') {
            return;
         }

         try {
            const result = await loadLocations();
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
            const result = await loadTalks({
               location
            });

            talksAtLocation = result?.guardians_talks ?? [];

            if (talkNameEl?.tagName === 'SELECT') {
               ConsoleDropdownPopulator.populateGuardiansTalkDropdown(
                  talkNameEl,
                  talksAtLocation
               );
            }

            refreshEnclosureOptions();
         }
         catch(err) {
         }
      }

      talkNameEl?.addEventListener('change', () => {
         refreshEnclosureOptions();
      });

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
