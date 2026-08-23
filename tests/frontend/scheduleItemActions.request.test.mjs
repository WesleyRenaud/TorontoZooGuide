import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildAnimalDraftEntry,
   buildAttractionDraftEntry,
   buildScheduleItemRequest,
} from '../../scripts/itinerary/panel/scheduleItemActions.js';
import { installScheduleItemActionsTestHooks } from './helpers/scheduleItemActionsTestSetup.mjs';

installScheduleItemActionsTestHooks();

test('buildAnimalDraftEntry and buildAttractionDraftEntry normalize rows', () => {
   assert.deepEqual(
      buildAnimalDraftEntry({ species: 'Tiger', exhibit: 'Savanna' }),
      { species: 'Tiger', exhibit: 'Savanna' }
   );
   assert.equal(buildAnimalDraftEntry({ species: 'Tiger' }), null);
   assert.equal(buildAttractionDraftEntry({ name: 'Carousel' }), 'Carousel');
   assert.equal(buildAttractionDraftEntry({ name: '' }), null);
});

test('buildScheduleItemRequest maps event and animal rows', () => {
   assert.deepEqual(
      buildScheduleItemRequest('lunch', null, ['lunch']),
      { itemType: 'lunch', key: '' }
   );
   assert.deepEqual(
      buildScheduleItemRequest('animals', {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      }, []),
      { itemType: 'animals', key: 'Tiger||Savanna' }
   );
   assert.deepEqual(
      buildScheduleItemRequest('attractions', {
         name: 'Zoomobile',
         added_as_attraction: true,
         scheduleItemKind: 'attractions',
      }, []),
      { itemType: 'attractions', key: 'Zoomobile' }
   );
   assert.deepEqual(
      buildScheduleItemRequest('transportations', {
         name: 'Zoomobile',
         added_as_attraction: false,
         scheduleItemKind: 'transportations',
      }, []),
      { itemType: 'transportations', key: 'Zoomobile||0' }
   );
});

test('buildScheduleItemRequest includes optional schedule times', () => {
   assert.deepEqual(
      buildScheduleItemRequest('lunch', null, ['lunch'], {
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
      buildScheduleItemRequest('animals', {
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
