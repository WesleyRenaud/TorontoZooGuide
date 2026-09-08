import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleItemController } from '../../../../scripts/itinerary/panel/scheduleItemController.js';
import { installScheduleItemActionsTestHooks } from '../../helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

test('Test_ScheduleItemActions_TestScheduleItemActionsBuildAnimalDraftEntryAndScheduleItemActionsBuildAttractionDraftEntryNormalizeRows_ExpectOk', () => {
   assert.deepEqual(
      ScheduleItemController.buildAnimalDraftEntry({ species: 'Tiger', exhibit: 'Savanna' }),
      { species: 'Tiger', exhibit: 'Savanna' }
   );
   assert.equal(ScheduleItemController.buildAnimalDraftEntry({ species: 'Tiger' }), null);
   assert.equal(ScheduleItemController.buildAttractionDraftEntry({ name: 'Carousel' }), 'Carousel');
   assert.equal(ScheduleItemController.buildAttractionDraftEntry({ name: '' }), null);
});

test('Test_ScheduleItemActions_TestScheduleItemActionsBuildScheduleItemRequestMapsEventAndAnimalRows_ExpectOk', () => {
   assert.deepEqual(
      ScheduleItemController.buildScheduleItemRequest('lunch', null, ['lunch']),
      { itemType: 'lunch', key: '' }
   );
   assert.deepEqual(
      ScheduleItemController.buildScheduleItemRequest('animals', {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      }, []),
      { itemType: 'animals', key: 'Tiger||Savanna' }
   );
   assert.deepEqual(
      ScheduleItemController.buildScheduleItemRequest('attractions', {
         name: 'Zoomobile',
         added_as_attraction: true,
         scheduleItemKind: 'attractions',
      }, []),
      { itemType: 'attractions', key: 'Zoomobile' }
   );
   assert.deepEqual(
      ScheduleItemController.buildScheduleItemRequest('transportations', {
         name: 'Zoomobile',
         added_as_attraction: false,
         scheduleItemKind: 'transportations',
      }, []),
      { itemType: 'transportations', key: 'Zoomobile||0' }
   );
});

test('Test_ScheduleItemActions_TestScheduleItemActionsBuildScheduleItemRequestIncludesOptionalScheduleTimes_ExpectOk', () => {
   assert.deepEqual(
      ScheduleItemController.buildScheduleItemRequest('lunch', null, ['lunch'], {
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
      ScheduleItemController.buildScheduleItemRequest('animals', {
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
