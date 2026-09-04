import assert from 'node:assert/strict';
import { test } from 'node:test';

import { saveItinerary } from '../../scripts/itinerary/itineraryServiceSave.js';
import { ItineraryErrorTypes } from '../../scripts/itinerary/itineraryErrorTypes.js';
import { StorageKeys } from '../../scripts/itinerary/storageKeys.js';
import { installItineraryServiceTestHooks } from './helpers/itineraryServiceTestSetup.mjs';

installItineraryServiceTestHooks();

test('saveItinerary includes selected exhibits in the backend payload', async () => {
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
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
         transportations: [],
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
      StorageKeys.SELECTED_EXHIBITS_KEY,
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

test('saveItinerary confirms before saving a guardians talk without a matching animal', async () => {
   const requests = [];
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WITHOUT_ANIMAL: 'guardiansTalkWithoutAnimal',
      },
      suppressed_error_types: [],
   };

   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
      errorTypes: itineraryConfig.itinerary_error_types,
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingGuardiansTalkWithoutAnimal
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'guardiansTalkWithoutAnimal',
            reasons: isConfirmed ? [] : [{
               code: 'guardiansTalkWithoutAnimal',
               items: [{
                  name: 'Komodo Dragon',
                  item_type: 'guardiansTalk',
                  start_time: '2:00 PM',
                  location: 'Australasia Pavilion',
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
      guardiansTalks: [{ name: 'Komodo Dragon' }],
      wildEncounters: [],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.match(
      popupMessage?.textContent ?? '',
      /The Komodo Dragon guardians talk at .* does not match an animal on your itinerary\. Do you still want to keep it on your plan\?/
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingGuardiansTalkWithoutAnimal, undefined);
   assert.equal(requests[1].body.confirmingGuardiansTalkWithoutAnimal, true);
});

test('saveItinerary confirms before saving an attraction without a matching animal', async () => {
   const requests = [];
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         ATTRACTION_WITHOUT_ANIMAL: 'attractionWithoutAnimal',
      },
      suppressed_error_types: [],
   };

   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
      errorTypes: itineraryConfig.itinerary_error_types,
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });

   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingAttractionWithoutAnimal
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : 'attractionWithoutAnimal',
            reasons: isConfirmed ? [] : [{
               code: 'attractionWithoutAnimal',
               items: [{
                  name: 'Kangaroo Walk-Thru',
                  item_type: 'attraction',
               }],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date: '2026-06-20',
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = saveItinerary({
      date: '2026-06-20',
      animals: [],
      attractions: ['Kangaroo Walk-Thru'],
      guardiansTalks: [],
      wildEncounters: [],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage?.textContent,
      'The Kangaroo Walk-Thru attraction does not match an animal on your itinerary. Do you still want to keep it on your plan?'
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingAttractionWithoutAnimal, undefined);
   assert.equal(requests[1].body.confirmingAttractionWithoutAnimal, true);
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
                  start_time: '10:00',
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
      /Adding the African Lion guardians talk will put it at .* on your day and update your walking route\. Your items will be rescheduled around it\./
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

test('saveItinerary returns cancelled when guardians talk reschedule is cancelled', async () => {
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: 'guardiansTalkWillUnscheduleItems',
      },
      suppressed_error_types: [],
   };

   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({
         status: 'guardiansTalkWillUnscheduleItems',
         reasons: [{
            code: 'guardiansTalkWillUnscheduleItems',
            items: [{
               name: 'Arctic Wolf',
               item_type: 'guardiansTalk',
               start_time: '11:00',
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
   });

   const savePromise = saveItinerary({
      date: '2026-06-15',
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: 'Arctic Wolf' }],
      wildEncounters: [],
   });

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   document.querySelector('.tzg-popup-cancel')?.click();

   const result = await savePromise;

   assert.deepEqual(result, {
      cancelled: true,
      issues: [{
         code: 'guardiansTalkWillUnscheduleItems',
         type: 'guardiansTalkWillUnscheduleItems',
         items: [{
            name: 'Arctic Wolf',
            item_type: 'guardiansTalk',
            start_time: '11:00',
         }],
      }],
   });
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
                  start_time: '14:00',
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
      /Adding the African Rainforest wild encounter will put it at .* on your day and update your walking route\. Your items will be rescheduled around it\./
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

   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
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

   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
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
      wildEncounters: [{ name: 'Grizzly Bear', start_time: '13:00' }],
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
   assert.equal(requests[1].body.wildEncounters[0], 'Grizzly Bear||13:00');
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

   ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
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

test('saveItinerary does not diff also-transportation attractions as removed', async () => {
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      assert.deepEqual(JSON.parse(options.body).transportations, [{
         name: 'Zoomobile',
         added_as_attraction: true,
      }]);

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'success',
            reasons: [],
            itinerary: {
               date: '2026-08-17',
               animals: [],
               attractions: [],
               transportations: [{
                  name: 'Zoomobile',
                  added_as_attraction: true,
                  likelihood: 100,
               }],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const result = await saveItinerary({
      date: '2026-08-17',
      animals: [],
      attractions: [{ name: 'Zoomobile', addedAsAttraction: true }],
      guardiansTalks: [],
      wildEncounters: [],
   });

   assert.deepEqual(result.validation.removed.attractions, []);
   assert.equal(result.validation.hasChanges, false);
});
