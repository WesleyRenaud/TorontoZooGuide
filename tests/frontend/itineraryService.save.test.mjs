import assert from 'node:assert/strict';
import { test } from 'node:test';

import { saveItinerary } from '../../scripts/itinerary/itineraryService.js';
import { updateItineraryErrorTypesFromConfig } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { SELECTED_EXHIBITS_KEY } from '../../scripts/itinerary/storageKeys.js';
import { installItineraryServiceTestHooks } from './helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();

test('saveItinerary includes selected exhibits in the backend payload', async () => {
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna', '  ', 'Eurasia'])
   );

   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      assert.deepEqual(JSON.parse(options.body), {
         date: '2026-06-15',
         arrivalTime: '',
         departureTime: '',
         animals: [],
         attractions: [],
         guardiansTalks: [],
         wildEncounters: [],
         selectedExhibits: ['Africa Savanna', 'Eurasia'],
         temp: null,
         overridingConflictingGuardiansTalks: false,
      });

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            reasons: [],
         }),
      };
   };

   await saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   }, {
      selectedExhibits: ['Africa Savanna', 'Eurasia'],
   });
});

test('saveItinerary omits selected exhibits by default', async () => {
   localStorage.setItem(
      SELECTED_EXHIBITS_KEY,
      JSON.stringify(['Africa Savanna'])
   );

   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      assert.deepEqual(JSON.parse(options.body).selectedExhibits, []);

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
            reasons: [],
         }),
      };
   };

   await saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   });
});

test('saveItinerary confirms before saving a guardians talk that unschedules items', async () => {
   const requests = [];
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'guardiansTalkWillUnscheduleItems',
      },
      suppressed_error_types: [],
   };

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingGuardiansTalkUnschedule
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'guardiansTalkWillUnscheduleItems',
            reasons: isConfirmed ? [] : [{
               code: 'guardiansTalkWillUnscheduleItems',
               items: [{
                  name: 'African Lion',
                  item_type: 'guardiansTalk',
               }],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: 'African Lion' }],
      wildEncounters: [],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.match(
      popupMessage?.textContent ?? '',
      /Adding these Meet the Guardians Talks: African Lion will unschedule other items/
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingGuardiansTalkUnschedule, undefined);
   assert.equal(requests[1].body.confirmingGuardiansTalkUnschedule, true);
});

test('saveItinerary confirms before saving a wild encounter that unschedules items', async () => {
   const requests = [];
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS: 'wildEncounterWillUnscheduleItems',
      },
      suppressed_error_types: [],
   };

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingWildEncounterUnschedule
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'wildEncounterWillUnscheduleItems',
            reasons: isConfirmed ? [] : [{
               code: 'wildEncounterWillUnscheduleItems',
               items: [{
                  name: 'African Rainforest',
                  item_type: 'wildEncounter',
               }],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [{ name: 'African Rainforest' }],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.match(
      popupMessage?.textContent ?? '',
      /Adding these Wild Encounters: African Rainforest will unschedule other items/
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingWildEncounterUnschedule, undefined);
   assert.equal(requests[1].body.confirmingWildEncounterUnschedule, true);
});

test('saveItinerary resolves schedule time conflicts before unschedule warnings', async () => {
   const requests = [];
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT: 'guardiansTalkWildEncounterTimeConflict',
         GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'guardiansTalkWillUnscheduleItems',
      },
      suppressed_error_types: [],
   };

   updateItineraryErrorTypesFromConfig({
      errorTypes: itineraryConfig.itinerary_error_types,
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const body = requests.at(-1)?.body ?? {};

      if (body.overridingConflictingGuardiansTalks) {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary_config: itineraryConfig,
               itinerary: {
                  date: '2026-06-15',
                  animals: [],
                  attractions: [],
                  guardians_talks: [{ name: 'African Lion' }],
                  wild_encounters: [],
               },
            }),
         };
      }

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'guardiansTalkWildEncounterTimeConflict',
            reasons: [{
               code: 'wildEncounterTimeConflict',
               items: [
                  {
                     name: 'African Lion',
                     item_type: 'guardiansTalk',
                     start_time: '14:00',
                     end_time: '14:30',
                     location: 'Africa Savanna',
                  },
                  {
                     name: 'African Rainforest',
                     item_type: 'wildEncounter',
                     start_time: '14:00',
                     end_time: '14:45',
                     meeting_spot: 'Wild Encounter - Africa Meeting Spot',
                  },
               ],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: 'African Lion' }],
      wildEncounters: [{ name: 'African Rainforest' }],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const conflictTitle = document.querySelector('.itin-top-title');

   assert.match(
      conflictTitle?.textContent ?? '',
      /Your Itinerary Has the Following Issues:/
   );

   document.querySelector('.itin-save-issue-select-btn')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.overridingConflictingGuardiansTalks, false);
   assert.equal(requests[1].body.overridingConflictingGuardiansTalks, true);
   assert.equal(requests[1].body.guardiansTalks.length, 1);
   assert.equal(requests[1].body.guardiansTalks[0].name, 'African Lion');
   assert.deepEqual(requests[1].body.wildEncounters, []);
});

test('saveItinerary does not diff unselected schedule conflicts as removals', async () => {
   const requests = [];
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT: 'guardiansTalkWildEncounterTimeConflict',
      },
      suppressed_error_types: [],
   };

   updateItineraryErrorTypesFromConfig({
      errorTypes: itineraryConfig.itinerary_error_types,
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const body = requests.at(-1)?.body ?? {};

      if (body.overridingConflictingGuardiansTalks) {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary_config: itineraryConfig,
               itinerary: {
                  date: '2026-06-15',
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [{ name: 'Grizzly Bear' }],
               },
            }),
         };
      }

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'guardiansTalkWildEncounterTimeConflict',
            reasons: [{
               code: 'wildEncounterTimeConflict',
               items: [
                  {
                     name: 'Highland Cattle',
                     item_type: 'guardiansTalk',
                     start_time: '13:00',
                     end_time: '13:30',
                     location: 'Eurasia Wilds',
                  },
                  {
                     name: 'Grizzly Bear',
                     item_type: 'wildEncounter',
                     start_time: '13:00',
                     end_time: '13:45',
                     meeting_spot: 'Wild Encounter - Americas Meeting Spot',
                  },
               ],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date: '2026-06-15',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: 'Highland Cattle' }],
      wildEncounters: [{ name: 'Grizzly Bear' }],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   document.body.querySelectorAll('.itin-save-issue-select-btn')[1]?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[1].body.overridingConflictingGuardiansTalks, true);
   assert.deepEqual(requests[1].body.guardiansTalks, []);
   assert.equal(requests[1].body.wildEncounters[0], 'Grizzly Bear');
   assert.deepEqual(result.validation.removed.guardiansTalks, []);
   assert.equal(result.validation.hasChanges, false);
});

test('saveItinerary preserves saved animals on conflict retry when payload omits them', async () => {
   const requests = [];
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT: 'guardiansTalkWildEncounterTimeConflict',
      },
      suppressed_error_types: [],
   };

   updateItineraryErrorTypesFromConfig({
      errorTypes: itineraryConfig.itinerary_error_types,
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const body = requests.at(-1)?.body ?? {};

      if (body.overridingConflictingGuardiansTalks) {
         return {
            ok: true,
            status: 200,
            statusText: 'OK',
            text: async () => JSON.stringify({
               status: 'success',
               reasons: [],
               itinerary_config: itineraryConfig,
               itinerary: {
                  date: '2026-06-15',
                  animals: [{
                     species: 'African Lion',
                     exhibit: 'Africa Savanna',
                     start_time: '14:30',
                     end_time: '14:45',
                  }],
                  attractions: [],
                  guardians_talks: [{ name: 'Nile Soft-Shelled Turtle' }],
                  wild_encounters: [],
               },
            }),
         };
      }

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'guardiansTalkWildEncounterTimeConflict',
            reasons: [{
               code: 'wildEncounterTimeConflict',
               items: [
                  {
                     name: 'Nile Soft-Shelled Turtle',
                     item_type: 'guardiansTalk',
                     start_time: '14:00',
                     end_time: '14:30',
                     location: 'African Rainforest Pavilion',
                  },
                  {
                     name: 'Guardians of White Rhinos',
                     item_type: 'wildEncounter',
                     start_time: '14:00',
                     end_time: '14:45',
                     meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
                  },
               ],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date: '2026-06-15',
               animals: [{
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '14:30',
                  end_time: '14:45',
               }],
               attractions: [],
               guardians_talks: [{ name: 'Nile Soft-Shelled Turtle' }],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: 'Nile Soft-Shelled Turtle' }],
      wildEncounters: [{ name: 'Guardians of White Rhinos' }],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   document.querySelector('.itin-save-issue-select-btn')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await savePromise;

   assert.equal(requests.length, 2);
   assert.deepEqual(requests[1].body.animals, [{
      species: 'African Lion',
      exhibit: 'Africa Savanna',
   }]);
});
