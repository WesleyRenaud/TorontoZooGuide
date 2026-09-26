import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItineraryServiceSaver } from '../../../scripts/itinerary/itineraryServiceSaver.js';
import { ItineraryErrorTypes } from '../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryItemFormatter } from '../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { WildEncounterScheduleItemKey } from '../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { StorageKeys } from '../../../scripts/itinerary/storageKeys.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installItineraryServiceTestHooks } from '../helpers/itineraryServiceTestSetup.mjs';
import { ItineraryErrorType } from '../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Strings } from '../../../scripts/strings.js';

installItineraryServiceTestHooks();


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryIncludesSelectedExhibitsInTheBackend_ExpectOk', async () => {
   const date = '2026-06-15';
   const africaSavanna = 'Africa Savanna';
   const eurasia = 'Eurasia';
   const selectedExhibits = [africaSavanna, eurasia];
   const draft = {
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([africaSavanna, '  ', eurasia])
   );
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      assert.deepEqual(JSON.parse(options.body), {
         date,
         arrivalTime: '',
         departureTime: '',
         animals: draft.animals,
         attractions: draft.attractions,
         transportations: [],
         guardiansTalks: draft.guardiansTalks,
         wildEncounters: draft.wildEncounters,
         selectedExhibits,
         temp: null,
         overridingConflictingGuardiansTalks: false,
         confirmingShortVisit: false,
         confirmingEarlyAdmission: false,
      });

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            itinerary: {
               date,
               animals: draft.animals,
               attractions: draft.attractions,
               guardians_talks: draft.guardiansTalks,
               wild_encounters: draft.wildEncounters,
            },
            reasons: [],
         }),
      };
   };

   await ItineraryServiceSaver.saveItinerary(draft, { selectedExhibits });
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryOmitsSelectedExhibitsByDefault_ExpectOk', async () => {
   const date = '2026-06-15';
   const africaSavanna = 'Africa Savanna';
   const draft = {
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
   };
   localStorage.setItem(
      StorageKeys.SELECTED_EXHIBITS_KEY,
      JSON.stringify([africaSavanna])
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
               date,
               animals: draft.animals,
               attractions: draft.attractions,
               guardians_talks: draft.guardiansTalks,
               wild_encounters: draft.wildEncounters,
            },
            reasons: [],
         }),
      };
   };

   await ItineraryServiceSaver.saveItinerary(draft);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryConfirmsBeforeSavingAGuardiansTalk_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-15';
   const talkName = 'Komodo Dragon';
   const startTime = '2:00 PM';
   const location = 'Australasia Pavilion';
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WITHOUT_ANIMAL: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      },
      suppressed_error_types: [],
   };
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });
   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(Position.LAST)?.body?.confirmingGuardiansTalkWithoutAnimal
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
            reasons: isConfirmed ? [] : [{
               code: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
               items: [{
                  name: talkName,
                  item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
                  start_time: startTime,
                  location,
               }],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: talkName }],
      wildEncounters: [],
   });
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage.textContent,
      Strings.itinerary.confirmation.guardiansTalkWithoutAnimalMessage(
         talkName,
         ItineraryItemFormatter.formatClockTime(startTime)
      )
   );

   document.querySelector('.tzg-popup-confirm')?.click();
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[Position.FIRST].body.confirmingGuardiansTalkWithoutAnimal, undefined);
   assert.equal(requests[Position.SECOND].body.confirmingGuardiansTalkWithoutAnimal, true);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryConfirmsBeforeSavingAnAttractionWithout_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-20';
   const attractionName = 'Kangaroo Walk-Thru';
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         ATTRACTION_WITHOUT_ANIMAL: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
      },
      suppressed_error_types: [],
   };
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });
   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(Position.LAST)?.body?.confirmingAttractionWithoutAnimal
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
            reasons: isConfirmed ? [] : [{
               code: ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
               items: [{
                  name: attractionName,
                  item_type: ItinerarySaveIssueItemType.ATTRACTION,
               }],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [attractionName],
      guardiansTalks: [],
      wildEncounters: [],
   });
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage?.textContent,
      `The ${attractionName} attraction does not match an animal on your itinerary. Do you still want to keep it on your plan?`
   );

   document.querySelector('.tzg-popup-confirm')?.click();
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[Position.FIRST].body.confirmingAttractionWithoutAnimal, undefined);
   assert.equal(requests[Position.SECOND].body.confirmingAttractionWithoutAnimal, true);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryConfirmsBeforeSavingAGuardiansTalk_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-15';
   const talkName = 'African Lion';
   const startTime = '10:00';
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      },
      suppressed_error_types: [],
   };
   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(Position.LAST)?.body?.confirmingGuardiansTalkUnschedule
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
            reasons: isConfirmed ? [] : [{
               code: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
               items: [{
                  name: talkName,
                  item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
                  start_time: startTime,
               }],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: talkName }],
      wildEncounters: [],
   });
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage.textContent,
      Strings.itinerary.confirmation.guardiansTalkRescheduleMessage(
         talkName,
         ItineraryItemFormatter.formatClockTime(startTime)
      )
   );

   document.querySelector('.tzg-popup-confirm')?.click();
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[Position.FIRST].body.confirmingGuardiansTalkUnschedule, undefined);
   assert.equal(requests[Position.SECOND].body.confirmingGuardiansTalkUnschedule, true);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryReturnsCancelledWhenGuardiansTalkReschedule_ExpectOk', async () => {
   const date = '2026-06-15';
   const talkName = 'Arctic Wolf';
   const startTime = '11:00';
   const errorType = ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS;
   const issueItem = {
      name: talkName,
      item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
      start_time: startTime,
   };
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: errorType,
      },
      suppressed_error_types: [],
   };
   globalThis.fetch = async () => ({
      ok: true,
      status: 200,
      statusText: 'OK',
      text: async () => JSON.stringify({
         status: errorType,
         reasons: [{
            code: errorType,
            items: [issueItem],
         }],
         itinerary_config: itineraryConfig,
         itinerary: {
            date,
            animals: [],
            attractions: [],
            guardians_talks: [],
            wild_encounters: [],
         },
      }),
   });

   const savePromise = ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: talkName }],
      wildEncounters: [],
   });
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   document.querySelector('.tzg-popup-cancel')?.click();
   const result = await savePromise;

   assert.equal(result.cancelled, true);
   assert.equal(result.issues[Position.FIRST].code, errorType);
   assert.equal(result.issues[Position.FIRST].type, errorType);
   assert.deepEqual(result.issues[Position.FIRST].items, [issueItem]);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryConfirmsBeforeSavingAWildEncounter_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-15';
   const encounterName = 'African Rainforest';
   const startTime = '14:00';
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
      },
      suppressed_error_types: [],
   };
   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const isConfirmed = Boolean(
         requests.at(Position.LAST)?.body?.confirmingWildEncounterUnschedule
      );

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: isConfirmed ? 'success' : ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
            reasons: isConfirmed ? [] : [{
               code: ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
               items: [{
                  name: encounterName,
                  item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
                  start_time: startTime,
               }],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [{ name: encounterName }],
   });
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage.textContent,
      Strings.itinerary.confirmation.wildEncounterRescheduleMessage(
         encounterName,
         ItineraryItemFormatter.formatClockTime(startTime)
      )
   );

   document.querySelector('.tzg-popup-confirm')?.click();
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[Position.FIRST].body.confirmingWildEncounterUnschedule, undefined);
   assert.equal(requests[Position.SECOND].body.confirmingWildEncounterUnschedule, true);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryResolvesScheduleTimeConflictsBeforeUnschedule_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-15';
   const talkName = 'African Lion';
   const encounterName = 'African Rainforest';
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT: ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
         GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      },
      suppressed_error_types: [],
   };
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });
   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const body = requests.at(Position.LAST)?.body ?? {};

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
                  date,
                  animals: [],
                  attractions: [],
                  guardians_talks: [{ name: talkName }],
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
            status: ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
            reasons: [{
               code: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
               items: [
                  {
                     name: talkName,
                     item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
                     start_time: '14:00',
                     end_time: '14:30',
                     location: 'Africa Savanna',
                  },
                  {
                     name: encounterName,
                     item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
                     start_time: '14:00',
                     end_time: '14:45',
                     meeting_spot: 'Wild Encounter - Africa Meeting Spot',
                  },
               ],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: talkName }],
      wildEncounters: [{ name: encounterName }],
   });
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   const conflictTitle = document.querySelector('.itin-top-title');

   assert.equal(
      conflictTitle.textContent,
      Strings.itinerary.confirmation.saveIssuesTitle
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
   assert.equal(requests[Position.FIRST].body.overridingConflictingGuardiansTalks, false);
   assert.equal(requests[Position.SECOND].body.overridingConflictingGuardiansTalks, true);
   assert.equal(requests[Position.SECOND].body.guardiansTalks.length, 1);
   assert.equal(requests[Position.SECOND].body.guardiansTalks[Position.FIRST].name, talkName);
   assert.deepEqual(requests[Position.SECOND].body.wildEncounters, []);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryDoesNotDiffUnselectedScheduleConflicts_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-15';
   const talkName = 'Highland Cattle';
   const encounterName = 'Grizzly Bear';
   const encounterStart = '13:00';
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT: ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
      },
      suppressed_error_types: [],
   };
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });
   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const body = requests.at(Position.LAST)?.body ?? {};

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
                  date,
                  animals: [],
                  attractions: [],
                  guardians_talks: [],
                  wild_encounters: [{ name: encounterName }],
               },
            }),
         };
      }

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
            reasons: [{
               code: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
               items: [
                  {
                     name: talkName,
                     item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
                     start_time: encounterStart,
                     end_time: '13:30',
                     location: 'Eurasia Wilds',
                  },
                  {
                     name: encounterName,
                     item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
                     start_time: encounterStart,
                     end_time: '13:45',
                     meeting_spot: 'Wild Encounter - Americas Meeting Spot',
                  },
               ],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date,
               animals: [],
               attractions: [],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: talkName }],
      wildEncounters: [{ name: encounterName, start_time: encounterStart }],
   });
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   document.body.querySelectorAll('.itin-save-issue-select-btn')[Position.SECOND]?.click();
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   document.querySelector('.tzg-popup-confirm')?.click();
   await new Promise((resolve) => {
      setTimeout(resolve, 0);
   });
   const result = await savePromise;

   assert.equal(requests.length, 2);
   assert.equal(requests[Position.SECOND].body.overridingConflictingGuardiansTalks, true);
   assert.deepEqual(requests[Position.SECOND].body.guardiansTalks, []);
   assert.equal(
      requests[Position.SECOND].body.wildEncounters[Position.FIRST],
      new WildEncounterScheduleItemKey(encounterName, encounterStart).toWire()
   );
   assert.deepEqual(result.validation.removed.guardiansTalks, []);
   assert.equal(result.validation.hasChanges, false);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryPreservesSavedAnimalsOnConflictRetry_ExpectOk', async () => {
   const requests = [];
   const date = '2026-06-15';
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const talkName = 'Nile Soft-Shelled Turtle';
   const encounterName = 'Guardians of White Rhinos';
   const scheduledAnimal = {
      species,
      exhibit,
      start_time: '14:30',
      end_time: '14:45',
   };
   const itineraryConfig = {
      itinerary_error_types: {
         SUCCESS: 'success',
         GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT: ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
      },
      suppressed_error_types: [],
   };
   ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
      suppressedErrorTypes: itineraryConfig.suppressed_error_types,
   });
   globalThis.fetch = async (url, options) => {
      requests.push({
         url,
         body: JSON.parse(options.body ?? '{}'),
      });

      const body = requests.at(Position.LAST)?.body ?? {};

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
                  date,
                  animals: [scheduledAnimal],
                  attractions: [],
                  guardians_talks: [{ name: talkName }],
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
            status: ItineraryErrorType.GUARDIANS_TALK_WILD_ENCOUNTER_TIME_CONFLICT,
            reasons: [{
               code: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
               items: [
                  {
                     name: talkName,
                     item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
                     start_time: '14:00',
                     end_time: '14:30',
                     location: 'African Rainforest Pavilion',
                  },
                  {
                     name: encounterName,
                     item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
                     start_time: '14:00',
                     end_time: '14:45',
                     meeting_spot: 'Wild Encounter - Penguin Meeting Spot',
                  },
               ],
            }],
            itinerary_config: itineraryConfig,
            itinerary: {
               date,
               animals: [scheduledAnimal],
               attractions: [],
               guardians_talks: [{ name: talkName }],
               wild_encounters: [],
            },
         }),
      };
   };

   const savePromise = ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [],
      guardiansTalks: [{ name: talkName }],
      wildEncounters: [{ name: encounterName }],
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
   assert.deepEqual(requests[Position.SECOND].body.animals, [{ species, exhibit }]);
});


test('Test_ItineraryServiceSave_TestItineraryServiceSaveSaveItineraryDoesNotDiffAlsoTransportationAttractions_ExpectOk', async () => {
   const date = '2026-08-17';
   const name = 'Zoomobile';
   const addedAsAttraction = true;
   globalThis.fetch = async (url, options) => {
      assert.equal(url, '/set-itinerary');
      assert.deepEqual(JSON.parse(options.body).transportations, [{
         name,
         added_as_attraction: addedAsAttraction,
      }]);

      return {
         ok: true,
         status: 200,
         statusText: 'OK',
         text: async () => JSON.stringify({
            status: 'success',
            reasons: [],
            itinerary: {
               date,
               animals: [],
               attractions: [],
               transportations: [{
                  name,
                  added_as_attraction: addedAsAttraction,
                  likelihood: 100,
               }],
               guardians_talks: [],
               wild_encounters: [],
            },
         }),
      };
   };

   const result = await ItineraryServiceSaver.saveItinerary({
      date,
      animals: [],
      attractions: [{ name, addedAsAttraction }],
      guardiansTalks: [],
      wildEncounters: [],
   });

   assert.deepEqual(result.validation.removed.attractions, []);
   assert.equal(result.validation.hasChanges, false);
});
