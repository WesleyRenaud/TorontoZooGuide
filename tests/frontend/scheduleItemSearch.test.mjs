import test from 'node:test';
import assert from 'node:assert/strict';

import {
   buildScheduleItemSearchPayload,
   extractScheduleItemSearchRows,
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
} from '../../scripts/itinerary/panel/scheduleItemSearch.js';
import {
   buildSchedulableEventTypes,
   buildScheduleItemTypeOptions,
   isScheduleItemEventType,
   isScheduleItemSearchEnabled,
   isScheduleItemTypeUnset,
   SCHEDULE_ITEM_MODULE_TYPES,
} from '../../scripts/itinerary/panel/scheduleItemTypes.js';

test('buildScheduleItemSearchPayload limits search to animals', () => {
   assert.deepEqual(
      buildScheduleItemSearchPayload(SCHEDULE_ITEM_MODULE_TYPES.animals, 'panda'),
      {
         query: 'panda',
         includeAnimals: true,
      }
   );
});

test('buildScheduleItemSearchPayload limits search to attractions', () => {
   assert.deepEqual(
      buildScheduleItemSearchPayload(SCHEDULE_ITEM_MODULE_TYPES.attractions, 'ride'),
      {
         query: 'ride',
         includeAttractions: true,
      }
   );
});

test('buildSchedulableEventTypes omits arrival and departure', () => {
   assert.deepEqual(
      buildSchedulableEventTypes({
         eventTypes: ['arrival', 'lunch', 'departure', 'break'],
      }),
      ['lunch', 'break']
   );
   assert.deepEqual(buildSchedulableEventTypes(null), []);
});

test('event type selections do not search animals or attractions', () => {
   assert.deepEqual(buildScheduleItemSearchPayload('lunch', 'snack'), {
      query: 'snack',
   });
   assert.deepEqual(
      extractScheduleItemSearchRows('lunch', {
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
         attractions: [{ name: 'Carousel' }],
      }),
      []
   );
});

test('placeholder search includes animals and attractions', () => {
   assert.deepEqual(buildScheduleItemSearchPayload('', 'tiger'), {
      query: 'tiger',
      includeAnimals: true,
      includeAttractions: true,
   });
});

test('type dropdown opens on a placeholder before event types and search kinds', () => {
   const options = buildScheduleItemTypeOptions(
      ['breakfast', 'lunch'],
      { typePlaceholder: 'Choose what to schedule' }
   );

   assert.deepEqual(options, [
      { value: '', label: 'Choose what to schedule', selected: true },
      { value: 'breakfast', label: 'Breakfast' },
      { value: 'lunch', label: 'Lunch' },
      { value: 'animals', label: 'Animal' },
      { value: 'attractions', label: 'Attraction' },
   ]);
});

test('placeholder enables global search; event types disable search', () => {
   const eventTypes = ['lunch', 'break'];

   assert.equal(isScheduleItemTypeUnset(''), true);
   assert.equal(isScheduleItemSearchEnabled('', eventTypes), true);
   assert.equal(isScheduleItemEventType('', eventTypes), false);
   assert.equal(isScheduleItemSearchEnabled('lunch', eventTypes), false);
   assert.equal(isScheduleItemEventType('lunch', eventTypes), true);
   assert.equal(
      isScheduleItemSearchEnabled(SCHEDULE_ITEM_MODULE_TYPES.animals, eventTypes),
      true
   );
   assert.equal(
      isScheduleItemSearchEnabled(SCHEDULE_ITEM_MODULE_TYPES.attractions, eventTypes),
      true
   );
});

test('extractScheduleItemSearchRows returns tagged rows for global search', () => {
   const response = {
      animals: [{ species: 'Giant Panda', exhibit: 'Bamboo' }],
      attractions: [{ name: 'Carousel' }],
   };

   assert.deepEqual(
      extractScheduleItemSearchRows('', response),
      [
         {
            species: 'Giant Panda',
            exhibit: 'Bamboo',
            scheduleItemKind: 'animals',
         },
         {
            name: 'Carousel',
            scheduleItemKind: 'attractions',
         },
      ]
   );
});

test('extractScheduleItemSearchRows returns only the selected collection', () => {
   const response = {
      animals: [{ species: 'Giant Panda', exhibit: 'Bamboo' }],
      attractions: [{ name: 'Carousel' }],
   };

   assert.deepEqual(
      extractScheduleItemSearchRows(SCHEDULE_ITEM_MODULE_TYPES.animals, response),
      [{
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: 'animals',
      }]
   );
   assert.deepEqual(
      extractScheduleItemSearchRows(SCHEDULE_ITEM_MODULE_TYPES.attractions, response),
      [{
         name: 'Carousel',
         scheduleItemKind: 'attractions',
      }]
   );
});

test('getScheduleItemRowKind and getScheduleItemRowId resolve mixed rows', () => {
   const animalRow = {
      species: 'Tiger',
      exhibit: 'Savanna',
      scheduleItemKind: 'animals',
   };
   const attractionRow = {
      name: 'Carousel',
      scheduleItemKind: 'attractions',
   };

   assert.equal(getScheduleItemRowKind(animalRow), 'animals');
   assert.equal(getScheduleItemRowKind(attractionRow), 'attractions');
   assert.equal(getScheduleItemRowId(animalRow), 'Tiger||Savanna');
   assert.equal(getScheduleItemRowId(attractionRow), 'Carousel');
});

test('resolveEffectiveScheduleItemSelection infers animals from a selected row', () => {
   const animalRow = {
      species: 'Pygmy Hippopotamus',
      exhibit: 'African Rainforest Pavilion',
      scheduleItemKind: 'animals',
   };

   assert.equal(
      resolveEffectiveScheduleItemSelection('', animalRow),
      SCHEDULE_ITEM_MODULE_TYPES.animals
   );
   assert.equal(
      resolveEffectiveScheduleItemSelection(
         SCHEDULE_ITEM_MODULE_TYPES.attractions,
         animalRow
      ),
      SCHEDULE_ITEM_MODULE_TYPES.attractions
   );
});
