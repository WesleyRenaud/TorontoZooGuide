import {
   postJson,
   populateGuardiansTalkDropdown
} from '../../utils.js';

export function createGuardiansTalkLocationFilterController({
   locationEl,
   talkNameEl,
} = {}) {

   function populateLocationDropdown(locations) {
      if (locationEl?.tagName !== 'SELECT') {
         return;
      }

      locationEl.innerHTML = '';

      const placeholder = document.createElement('option');
      placeholder.value = '';
      placeholder.textContent = 'Select a location';
      locationEl.appendChild(placeholder);

      locations
         .slice()
         .sort((a, b) => {
            const aName =
               typeof a === 'string'
                  ? a
                  : String(a.location ?? a.LOCATION ?? a.name ?? a.NAME ?? '');

            const bName =
               typeof b === 'string'
                  ? b
                  : String(b.location ?? b.LOCATION ?? b.name ?? b.NAME ?? '');

            return aName.localeCompare(bName);
         })
         .forEach(location => {
            const name =
               typeof location === 'string'
                  ? location
                  : location.location ?? location.LOCATION ?? location.name ?? location.NAME ?? '';

            if (!name) return;

            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            locationEl.appendChild(option);
         });
   }

   function clearTalkDropdown() {
      if (talkNameEl?.tagName === 'SELECT') {
         populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if (talkNameEl) {
         talkNameEl.value = '';
      }
   }

   async function loadLocations() {
      if (locationEl?.tagName !== 'SELECT') {
         return;
      }

      try {
         const result = await postJson('/get-guardians-talk-locations', {});
         const guardiansTalkLocations = result?.guardians_talk_locations ?? [];
         populateLocationDropdown(guardiansTalkLocations);
      }
      catch(err) {
      }
   }

   async function loadTalksForSelectedLocation() {
      const location = locationEl?.value.trim() ?? '';

      clearTalkDropdown();

      if (!location) {
         return;
      }

      try {
         const result = await postJson('/get-guardians-talk-names-at-location', {
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

      loadTalksForSelectedLocation();
   });

   return {
      refreshLocations: loadLocations,
      refresh: loadTalksForSelectedLocation,
      clear() {
         clearTalkDropdown();
      }
   };
}