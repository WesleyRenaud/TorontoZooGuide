import assert from 'node:assert/strict';
import { test } from 'node:test';

import { scheduleSelectedItineraryItem } from '../../scripts/itinerary/panel/scheduleItemActions.js';
import {
   MOCK_ERROR_TYPES,
   mockJsonResponse,
   mockScheduleItemFetch,
   installScheduleItemActionsTestHooks,
} from './helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

function mockItineraryDateResponse() {
   return mockJsonResponse({ date: '2026-06-15' });
}

test('scheduleSelectedItineraryItem persists suppression before confirming', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      if (url === '/get-itinerary-date') {
         return mockItineraryDateResponse();
      }

      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      if (url === '/suppress-itinerary-warning') {
         return mockJsonResponse({
            status: 'success',
            suppressed_warnings: [],
            itinerary_config: {
               itinerary_error_types: MOCK_ERROR_TYPES,
               suppressed_error_types: ['itemNotOnItinerary'],
            },
         });
      }

      const isConfirmed = Boolean(
         requests.filter((request) => request.url === '/schedule-itinerary-item').at(-1)
            ?.body?.confirmingScheduleItemNotOnItinerary
      );

      return mockJsonResponse({
         status: isConfirmed ? 'success' : 'itemNotOnItinerary',
         reasons: [],
      });
   };

   const schedulePromise = scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'animals',
      { species: 'Tiger', exhibit: 'Savanna', scheduleItemKind: 'animals' },
      []
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const label = document.querySelector('.tzg-popup-do-not-show-again');
   const confirmButton = document.querySelector('.tzg-popup-confirm');
   const checkbox = label?.children?.find((child) => child.tagName === 'input');

   assert.ok(checkbox);
   assert.ok(confirmButton);
   checkbox.checked = true;
   confirmButton.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await schedulePromise;

   assert.equal(result.errorType, 'success');
   assert.deepEqual(
      requests.map((request) => request.url),
      [
         '/schedule-itinerary-item',
         '/suppress-itinerary-warning',
         '/schedule-itinerary-item',
      ]
   );
   assert.equal(requests[1].body.warningType, 'itemNotOnItinerary');
   assert.equal(requests[2].body.confirmingScheduleItemNotOnItinerary, true);
   assert.equal(
      requests[2].body.suppressScheduleItemNotOnItineraryWarning,
      undefined
   );
});

test('scheduleSelectedItineraryItem confirms before scheduling a new animal', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      if (url === '/get-itinerary-date') {
         return mockItineraryDateResponse();
      }

      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingScheduleItemNotOnItinerary
      );

      return mockJsonResponse({
         status: isConfirmed ? 'success' : 'itemNotOnItinerary',
         reasons: isConfirmed ? [] : [],
      });
   };

   const schedulePromise = scheduleSelectedItineraryItem(
      { date: '2026-06-15', animals: [], attractions: [] },
      'animals',
      { species: 'Tiger', exhibit: 'Savanna', scheduleItemKind: 'animals' },
      []
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const confirmButton = document.querySelector('.tzg-popup-confirm');

   assert.ok(confirmButton);
   confirmButton.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await schedulePromise;

   assert.equal(result.errorType, 'success');
   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingScheduleItemNotOnItinerary, false);
   assert.equal(requests[1].body.confirmingScheduleItemNotOnItinerary, true);
});

test('scheduleSelectedItineraryItem confirms before scheduling a talk without matching animal', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      if (url === '/get-itinerary-date') {
         return mockItineraryDateResponse();
      }

      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingGuardiansTalkWithoutAnimal
      );

      return mockJsonResponse({
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
      });
   };

   const schedulePromise = scheduleSelectedItineraryItem(
      {
         date: '2026-06-15',
         animals: [],
         attractions: [],
         guardiansTalks: [{ name: 'Komodo Dragon' }],
      },
      'guardians_talks',
      { name: 'Komodo Dragon', scheduleItemKind: 'guardians_talks' },
      []
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const confirmButton = document.querySelector('.tzg-popup-confirm');
   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.ok(confirmButton);
   assert.match(
      popupMessage?.textContent ?? '',
      /The Komodo Dragon guardians talk at .* does not match an animal on your itinerary\. Do you still want to keep it on your plan\?/
   );
   confirmButton.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await schedulePromise;

   assert.equal(result.errorType, 'success');
   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingGuardiansTalkWithoutAnimal, false);
   assert.equal(requests[1].body.confirmingGuardiansTalkWithoutAnimal, true);
});

test('scheduleSelectedItineraryItem confirms before scheduling a guardians talk', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      if (url === '/get-itinerary-date') {
         return mockItineraryDateResponse();
      }

      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingGuardiansTalkUnschedule
      );

      return mockJsonResponse({
         status: isConfirmed ? 'success' : 'guardiansTalkWillUnscheduleItems',
         reasons: isConfirmed ? [] : [{
            code: 'guardiansTalkWillUnscheduleItems',
            items: [{
               name: 'African Lion',
               item_type: 'guardiansTalk',
               start_time: '10:00',
            }],
         }],
      });
   };

   const schedulePromise = scheduleSelectedItineraryItem(
      {
         date: '2026-06-15',
         animals: [{ species: 'Tiger', exhibit: 'Savanna', start_time: '10:00' }],
         attractions: [],
         guardiansTalks: [{ name: 'African Lion' }],
      },
      'guardians_talks',
      { name: 'African Lion', scheduleItemKind: 'guardians_talks' },
      []
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const confirmButton = document.querySelector('.tzg-popup-confirm');
   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.ok(confirmButton);
   assert.match(
      popupMessage?.textContent ?? '',
      /Adding the African Lion guardians talk will put it at .* on your day and update your walking route\. Your items will be rescheduled around it\./
   );
   confirmButton.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await schedulePromise;

   assert.equal(result.errorType, 'success');
   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingGuardiansTalkUnschedule, false);
   assert.equal(requests[1].body.confirmingGuardiansTalkUnschedule, true);
});

test('scheduleSelectedItineraryItem returns cancelled when guardians talk reschedule is declined', async () => {
   globalThis.fetch = mockScheduleItemFetch({
      routes: {
         '/schedule-itinerary-item': {
            status: 'guardiansTalkWillUnscheduleItems',
            reasons: [{
               code: 'guardiansTalkWillUnscheduleItems',
               items: [{
                  name: 'Arctic Wolf',
                  item_type: 'guardiansTalk',
                  start_time: '11:00',
               }],
            }],
         },
      },
   });

   const schedulePromise = scheduleSelectedItineraryItem(
      {
         date: '2026-06-15',
         animals: [{ species: 'Tiger', exhibit: 'Savanna', start_time: '11:00' }],
         attractions: [],
         guardiansTalks: [{ name: 'Arctic Wolf' }],
      },
      'guardians_talks',
      { name: 'Arctic Wolf', scheduleItemKind: 'guardians_talks' },
      []
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   document.querySelector('.tzg-popup-cancel')?.click();

   const result = await schedulePromise;

   assert.equal(result.cancelled, true);
   assert.equal(result.errorType, 'guardiansTalkWillUnscheduleItems');
});

test('scheduleSelectedItineraryItem confirms before scheduling a wild encounter', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      if (url === '/get-itinerary-date') {
         return mockItineraryDateResponse();
      }

      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingWildEncounterUnschedule
      );

      return mockJsonResponse({
         status: isConfirmed ? 'success' : 'wildEncounterWillUnscheduleItems',
         reasons: isConfirmed ? [] : [{
            code: 'wildEncounterWillUnscheduleItems',
            items: [{
               name: 'African Rainforest',
               item_type: 'wildEncounter',
               start_time: '14:00',
            }],
         }],
      });
   };

   const schedulePromise = scheduleSelectedItineraryItem(
      {
         date: '2026-06-15',
         animals: [{ species: 'Tiger', exhibit: 'Savanna', start_time: '14:00' }],
         attractions: [],
         wildEncounters: [{ name: 'African Rainforest' }],
      },
      'wild_encounters',
      { name: 'African Rainforest', start_time: '14:00', scheduleItemKind: 'wild_encounters' },
      []
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const confirmButton = document.querySelector('.tzg-popup-confirm');
   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.ok(confirmButton);
   assert.match(
      popupMessage?.textContent ?? '',
      /Adding the African Rainforest wild encounter will put it at .* on your day and update your walking route\. Your items will be rescheduled around it\./
   );
   confirmButton.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await schedulePromise;

   assert.equal(result.errorType, 'success');
   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingWildEncounterUnschedule, false);
   assert.equal(requests[1].body.confirmingWildEncounterUnschedule, true);
});

test('scheduleSelectedItineraryItem confirms multiple build warnings together', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      if (url === '/get-itinerary-date') {
         return mockItineraryDateResponse();
      }

      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const body = requests.at(-1)?.body ?? {};
      const isConfirmed = Boolean(
         body.confirmingGuardiansTalkUnschedule
         && body.confirmingGuardiansTalkWithoutAnimal
      );

      return mockJsonResponse({
         status: isConfirmed ? 'success' : 'guardiansTalkWillUnscheduleItems',
         reasons: isConfirmed ? [] : [
            {
               code: 'guardiansTalkWillUnscheduleItems',
               items: [{
                  name: 'Amur Tiger',
                  item_type: 'guardiansTalk',
                  start_time: '11:00 AM',
               }],
            },
            {
               code: 'guardiansTalkWithoutAnimal',
               items: [{
                  name: 'Amur Tiger',
                  item_type: 'guardiansTalk',
                  start_time: '11:00 AM',
               }],
            },
         ],
      });
   };

   const schedulePromise = scheduleSelectedItineraryItem(
      {
         date: '2026-06-15',
         animals: [{ species: 'African Lion', exhibit: 'Africa Savanna', start_time: '11:00 AM' }],
         attractions: [],
         guardiansTalks: [],
      },
      'guardians_talks',
      {
         name: 'Amur Tiger',
         start_time: '11:00 AM',
         scheduleItemKind: 'guardians_talks',
      },
      []
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   assert.equal(
      document.querySelector('.itin-top-title')?.textContent,
      'Your Itinerary Has the Following Issues:'
   );
   assert.equal(
      document.querySelectorAll('.itin-build-warning-module').length,
      2
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await schedulePromise;

   assert.equal(result.errorType, 'success');
   assert.equal(requests.length, 2);
   assert.equal(requests[1].body.confirmingGuardiansTalkUnschedule, true);
   assert.equal(requests[1].body.confirmingGuardiansTalkWithoutAnimal, true);
});

test('scheduleSelectedItineraryItem adjusts attraction outside operating hours', async () => {
   const requests = [];

   globalThis.fetch = async (url, options = {}) => {
      if (url === '/get-itinerary-date') {
         return mockItineraryDateResponse();
      }

      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(-1)?.body?.confirmingAttractionOutsideOperatingHours
      );

      return mockJsonResponse({
         status: isConfirmed ? 'success' : 'attractionOutsideOperatingHours',
         reasons: [],
      });
   };

   const schedulePromise = scheduleSelectedItineraryItem(
      {
         date: '2026-06-15',
         animals: [],
         attractions: [{ name: 'Splash Island' }],
      },
      'attractions',
      {
         name: 'Splash Island',
         scheduleItemKind: 'attractions',
      },
      [],
      {
         startTime: '10:00 AM',
      }
   );

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const title = document.querySelector('.itin-top-title');
   const confirmButton = document.querySelector('.tzg-popup-confirm');
   const cancelButton = document.querySelector('.tzg-popup-cancel');

   assert.equal(title?.textContent, 'Outside Attraction Hours');
   assert.equal(confirmButton?.textContent, 'Adjust');
   assert.equal(cancelButton?.textContent, 'Cancel');
   confirmButton.click();

   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });

   const result = await schedulePromise;

   assert.equal(result.errorType, 'success');
   assert.equal(requests.length, 2);
   assert.equal(requests[0].body.confirmingAttractionOutsideOperatingHours, false);
   assert.equal(requests[1].body.confirmingAttractionOutsideOperatingHours, true);
   assert.equal(requests[1].body.startTime, '10:00 AM');
});
