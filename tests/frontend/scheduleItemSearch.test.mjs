import test from 'node:test';
import assert from 'node:assert/strict';

import {
   buildItineraryScheduleItemRowIds,
   buildScheduleItemSearchPayload,
   extractScheduleItemSearchRows,
   filterScheduleItemRowsToItinerary,
   getScheduleItemRowId,
   getScheduleItemRowKind,
   resolveEffectiveScheduleItemSelection,
   tagScheduleItemRow,
} from '../../scripts/itinerary/panel/scheduleItemSearch.js';
import {
   buildSchedulableEventTypes,
   buildScheduleItemTypeOptions,
   isScheduleItemEventType,
   isScheduleItemSearchEnabled,
   isScheduleItemTypeUnset,
} from '../../scripts/itinerary/panel/scheduleItemTypes.js';
import { ScheduleItemKind } from '../../scripts/shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../scripts/strings.js';

test('buildScheduleItemSearchPayload limits search to animals', () => {
   assert.deepEqual(
      buildScheduleItemSearchPayload(ScheduleItemKind.ANIMAL.itemType, 'panda'),
      {
         query: 'panda',
         includeAnimals: true,
      }
   );
});

test('buildScheduleItemSearchPayload limits search to attractions', () => {
   assert.deepEqual(
      buildScheduleItemSearchPayload(ScheduleItemKind.ATTRACTION.itemType, 'ride'),
      {
         query: 'ride',
         includeAttractions: true,
      }
   );
});

test('buildScheduleItemSearchPayload limits search to wild encounters', () => {
   assert.deepEqual(
      buildScheduleItemSearchPayload(ScheduleItemKind.WILD_ENCOUNTER.itemType, 'rainforest'),
      {
         query: 'rainforest',
         includeWildEncounters: true,
      }
   );
});

test('buildScheduleItemSearchPayload limits search to guardians talks', () => {
   assert.deepEqual(
      buildScheduleItemSearchPayload(ScheduleItemKind.GUARDIANS_TALK.itemType, 'tiger'),
      {
         query: 'tiger',
         includeGuardiansTalks: true,
      }
   );
});

test('buildSchedulableEventTypes omits arrival and departure', () => {
   assert.deepEqual(
      buildSchedulableEventTypes({
         eventTypes: ['arrival', 'lunch', 'departure', 'break'],
         visitBoundaryEventTypes: {
            arrival: 'arrival',
            departure: 'departure',
         },
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

test('placeholder search includes searchable schedule item kinds', () => {
   assert.deepEqual(buildScheduleItemSearchPayload('', 'tiger'), {
      query: 'tiger',
      includeAnimals: true,
      includeAttractions: true,
      includeGuardiansTalks: true,
      includeWildEncounters: true,
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
      { value: 'animals', label: APP_STRINGS.entityLabels.animal },
      { value: 'attractions', label: APP_STRINGS.entityLabels.attraction },
      {
         value: 'guardians_talks',
         label: APP_STRINGS.entityLabels.guardiansTalk,
      },
      {
         value: 'wild_encounters',
         label: APP_STRINGS.entityLabels.wildEncounter,
      },
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
      isScheduleItemSearchEnabled(ScheduleItemKind.ANIMAL.itemType, eventTypes),
      true
   );
   assert.equal(
      isScheduleItemSearchEnabled(ScheduleItemKind.ATTRACTION.itemType, eventTypes),
      true
   );
   assert.equal(
      isScheduleItemSearchEnabled(ScheduleItemKind.GUARDIANS_TALK.itemType, eventTypes),
      true
   );
   assert.equal(
      isScheduleItemSearchEnabled(ScheduleItemKind.WILD_ENCOUNTER.itemType, eventTypes),
      true
   );
});

test('extractScheduleItemSearchRows returns tagged rows for global search', () => {
   const response = {
      animals: [{ species: 'Giant Panda', exhibit: 'Bamboo' }],
      attractions: [{ name: 'Carousel' }],
      guardians_talks: [{ name: 'Amur Tiger', location: 'Eurasia Wilds' }],
      wild_encounters: [{ name: 'African Rainforest', meeting_spot: 'Africa' }],
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
         {
            name: 'Amur Tiger',
            location: 'Eurasia Wilds',
            scheduleItemKind: 'guardians_talks',
         },
         {
            name: 'African Rainforest',
            meeting_spot: 'Africa',
            scheduleItemKind: 'wild_encounters',
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
      extractScheduleItemSearchRows(ScheduleItemKind.ANIMAL.itemType, response),
      [{
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: 'animals',
      }]
   );
   assert.deepEqual(
      extractScheduleItemSearchRows(ScheduleItemKind.ATTRACTION.itemType, response),
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
   const guardiansTalkRow = {
      name: 'Amur Tiger',
      scheduleItemKind: 'guardians_talks',
   };
   const wildEncounterRow = {
      name: 'African Rainforest',
      scheduleItemKind: 'wild_encounters',
   };

   assert.equal(getScheduleItemRowKind(animalRow), 'animals');
   assert.equal(getScheduleItemRowKind(attractionRow), 'attractions');
   assert.equal(getScheduleItemRowKind(guardiansTalkRow), 'guardians_talks');
   assert.equal(getScheduleItemRowKind(wildEncounterRow), 'wild_encounters');
   assert.equal(getScheduleItemRowId(animalRow), 'Tiger||Savanna');
   assert.equal(getScheduleItemRowId(attractionRow), 'Carousel');
   assert.equal(getScheduleItemRowId(guardiansTalkRow), 'Amur Tiger');
   assert.equal(getScheduleItemRowId(wildEncounterRow), 'African Rainforest');
});

test('resolveEffectiveScheduleItemSelection infers animals from a selected row', () => {
   const animalRow = {
      species: 'Pygmy Hippopotamus',
      exhibit: 'African Rainforest Pavilion',
      scheduleItemKind: 'animals',
   };

   assert.equal(
      resolveEffectiveScheduleItemSelection('', animalRow),
      ScheduleItemKind.ANIMAL.itemType
   );
   assert.equal(
      resolveEffectiveScheduleItemSelection(
         ScheduleItemKind.ATTRACTION.itemType,
         animalRow
      ),
      ScheduleItemKind.ATTRACTION.itemType
   );
});

test('buildItineraryScheduleItemRowIds collects schedule item keys', () => {
   const ids = buildItineraryScheduleItemRowIds({
      animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
      attractions: [{ name: 'Carousel' }],
      guardiansTalks: [{ name: 'Amur Tiger', start_time: '1:30 PM' }],
      wildEncounters: [
         { name: 'African Rainforest', start_time: '' },
         { name: 'Americas', start_time: '2:00 PM' },
      ],
   });

   assert.equal(ids.animalIds.has('Tiger||Savanna'), true);
   assert.equal(ids.attractionIds.has('Carousel'), true);
   assert.equal(ids.guardiansTalkIds.has('Amur Tiger'), true);
   assert.equal(ids.wildEncounterIds.has('African Rainforest'), true);
   assert.equal(ids.wildEncounterIds.has('Americas'), true);
});

test('buildItineraryScheduleItemRowIds can exclude scheduled items', () => {
   const ids = buildItineraryScheduleItemRowIds({
      animals: [
         { species: 'Tiger', exhibit: 'Savanna', start_time: '1:00 PM' },
         { species: 'Giant Panda', exhibit: 'Bamboo' },
      ],
      guardiansTalks: [
         { name: 'Amur Tiger', start_time: '1:30 PM' },
         { name: 'Polar Bear', start_time: '' },
      ],
   }, { unscheduledOnly: true });

   assert.equal(ids.animalIds.has('Tiger||Savanna'), false);
   assert.equal(ids.animalIds.has('Giant Panda||Bamboo'), true);
   assert.equal(ids.guardiansTalkIds.has('Amur Tiger'), false);
   assert.equal(ids.guardiansTalkIds.has('Polar Bear'), true);
});

test('filterScheduleItemRowsToItinerary keeps only rows on the itinerary', () => {
   const rows = [
      {
         species: 'Tiger',
         exhibit: 'Savanna',
         scheduleItemKind: 'animals',
      },
      {
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: 'animals',
      },
      {
         name: 'Carousel',
         scheduleItemKind: 'attractions',
      },
      {
         name: 'Train',
         scheduleItemKind: 'attractions',
      },
      {
         name: 'Amur Tiger',
         scheduleItemKind: 'guardians_talks',
      },
      {
         name: 'Polar Bear',
         scheduleItemKind: 'guardians_talks',
      },
      {
         name: 'African Rainforest',
         scheduleItemKind: 'wild_encounters',
      },
   ];

   assert.deepEqual(
      filterScheduleItemRowsToItinerary(rows, {
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
         attractions: [{ name: 'Carousel' }],
         guardiansTalks: [{ name: 'Amur Tiger' }],
         wildEncounters: [{ name: 'African Rainforest' }],
      }),
      [
         {
            species: 'Tiger',
            exhibit: 'Savanna',
            scheduleItemKind: 'animals',
         },
         {
            name: 'Carousel',
            scheduleItemKind: 'attractions',
         },
         {
            name: 'Amur Tiger',
            scheduleItemKind: 'guardians_talks',
         },
         {
            name: 'African Rainforest',
            scheduleItemKind: 'wild_encounters',
         },
      ]
   );
});

test('tagScheduleItemRow tags itinerary rows for the schedule module', () => {
   const animalRow = tagScheduleItemRow(ScheduleItemKind.ANIMAL.itemType, {
      species: 'Giant Panda',
      exhibit: 'Eurasia Wilds',
   });
   const attractionRow = tagScheduleItemRow(ScheduleItemKind.ATTRACTION.itemType, {
      name: 'Conservation Carousel',
   });
   const guardiansTalkRow = tagScheduleItemRow(ScheduleItemKind.GUARDIANS_TALK.itemType, {
      name: 'Amur Tiger',
   });

   assert.equal(animalRow.scheduleItemKind, ScheduleItemKind.ANIMAL.itemType);
   assert.equal(
      getScheduleItemRowId(animalRow),
      'Giant Panda||Eurasia Wilds'
   );
   assert.equal(attractionRow.scheduleItemKind, ScheduleItemKind.ATTRACTION.itemType);
   assert.equal(getScheduleItemRowId(attractionRow), 'Conservation Carousel');
   assert.equal(
      guardiansTalkRow.scheduleItemKind,
      ScheduleItemKind.GUARDIANS_TALK.itemType
   );
   assert.equal(getScheduleItemRowId(guardiansTalkRow), 'Amur Tiger');
   assert.equal(tagScheduleItemRow(ScheduleItemKind.ANIMAL.itemType, null), null);
});
