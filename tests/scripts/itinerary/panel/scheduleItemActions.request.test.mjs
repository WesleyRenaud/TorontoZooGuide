import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemActions } from '../../../../scripts/itinerary/panel/scheduleItemActions.js';
import { installScheduleItemActionsTestHooks } from '../../helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

test('Test_ScheduleItemActions_TestScheduleItemActionsBuildAnimalDraftEntryAndScheduleItemActionsBuildAttractionDraftEntryNormalizeRows_ExpectOk', () => {
   assert.deepEqual(
      ScheduleItemActions.buildAnimalDraftEntry({ species: 'Tiger', exhibit: 'Savanna' }),
      { species: 'Tiger', exhibit: 'Savanna' }
   );
   assert.equal(ScheduleItemActions.buildAnimalDraftEntry({ species: 'Tiger' }), null);
   assert.equal(ScheduleItemActions.buildAttractionDraftEntry({ name: 'Carousel' }), 'Carousel');
   assert.equal(ScheduleItemActions.buildAttractionDraftEntry({ name: '' }), null);
});

test('Test_ScheduleItemActions_TestScheduleItemActionsBuildScheduleItemRequestMapsEventAndAnimalRows_ExpectOk', () => {
   assert.deepEqual(
      ScheduleItemActions.buildScheduleItemRequest('lunch', null, ['lunch']),
      { itemType: 'lunch', key: '' }
   );
   assert.deepEqual(
      ScheduleItemActions.buildScheduleItemRequest('animals', {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      }, []),
      { itemType: 'animals', key: 'Tiger||Savanna' }
   );
   assert.deepEqual(
      ScheduleItemActions.buildScheduleItemRequest('attractions', {
         name: 'Zoomobile',
         added_as_attraction: true,
         scheduleItemKind: 'attractions',
      }, []),
      { itemType: 'attractions', key: 'Zoomobile' }
   );
   assert.deepEqual(
      ScheduleItemActions.buildScheduleItemRequest('transportations', {
         name: 'Zoomobile',
         added_as_attraction: false,
         scheduleItemKind: 'transportations',
      }, []),
      { itemType: 'transportations', key: 'Zoomobile||0' }
   );
});

test('Test_ScheduleItemActions_TestScheduleItemActionsBuildScheduleItemRequestIncludesOptionalScheduleTimes_ExpectOk', () => {
   assert.deepEqual(
      ScheduleItemActions.buildScheduleItemRequest('lunch', null, ['lunch'], {
         startTime: '10:00 AM',
         durationMinutes: 20,
      }),
      {
         itemType: 'lunch',
         key: '',
         startTime: '10:00 AM',
         durationMinutes: 20,
      }
   );
   assert.deepEqual(
      ScheduleItemActions.buildScheduleItemRequest('animals', {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      }, [], { durationMinutes: 20 }),
      {
         itemType: 'animals',
         key: 'Tiger||Savanna',
         durationMinutes: 20,
      }
   );
});
