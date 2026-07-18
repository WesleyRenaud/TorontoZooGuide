import test from 'node:test';
import assert from 'node:assert/strict';

import {
   buildItineraryScheduleItemRowIds,
   buildScheduleItemSearchPayload,
   extractScheduleItemSearchRows,
   filterScheduleItemRowsExcludingScheduledOccurrences,
   filterScheduleItemRowsForScheduleModule,
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
         forItinerary: true,
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
      forItinerary: true,
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
      start_time: '14:00',
      scheduleItemKind: 'guardians_talks',
   };
   const wildEncounterRow = {
      name: 'African Rainforest',
      start_time: '14:00',
      scheduleItemKind: 'wild_encounters',
   };

   assert.equal(getScheduleItemRowKind(animalRow), 'animals');
   assert.equal(getScheduleItemRowKind(attractionRow), 'attractions');
   assert.equal(getScheduleItemRowKind(guardiansTalkRow), 'guardians_talks');
   assert.equal(getScheduleItemRowKind(wildEncounterRow), 'wild_encounters');
   assert.equal(getScheduleItemRowId(animalRow), 'Tiger||Savanna');
   assert.equal(getScheduleItemRowId(attractionRow), 'Carousel');
   assert.equal(getScheduleItemRowId(guardiansTalkRow), 'Amur Tiger||14:00');
   assert.equal(getScheduleItemRowId(wildEncounterRow), 'African Rainforest||14:00');
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
   assert.equal(ids.guardiansTalkIds.has('Amur Tiger||1:30 PM'), true);
   assert.equal(ids.wildEncounterIds.has('African Rainforest'), false);
   assert.equal(ids.wildEncounterIds.has('Americas||2:00 PM'), true);
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
   assert.equal(ids.guardiansTalkIds.has('Amur Tiger||1:30 PM'), false);
   assert.equal(ids.guardiansTalkIds.has(''), true);
});

test('buildItineraryScheduleItemRowIds can include scheduled items only', () => {
   const ids = buildItineraryScheduleItemRowIds({
      guardiansTalks: [
         { name: 'Amur Tiger', start_time: '1:30 PM' },
         { name: 'Polar Bear', start_time: '' },
      ],
      wildEncounters: [
         { name: 'African Rainforest', start_time: '2:00 PM' },
      ],
   }, { scheduledOnly: true });

   assert.equal(ids.guardiansTalkIds.has('Amur Tiger||1:30 PM'), true);
   assert.equal(ids.guardiansTalkIds.has(''), false);
   assert.equal(ids.wildEncounterIds.has('African Rainforest||2:00 PM'), true);
});

test('filterScheduleItemRowsExcludingScheduledOccurrences hides scheduled guest and fixed-time items', () => {
   const rows = [
      {
         name: 'Amur Tiger',
         start_time: '1:30 PM',
         scheduleItemKind: 'guardians_talks',
      },
      {
         name: 'Polar Bear',
         start_time: '2:00 PM',
         scheduleItemKind: 'guardians_talks',
      },
      {
         name: 'African Rainforest',
         start_time: '2:00 PM',
         scheduleItemKind: 'wild_encounters',
      },
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
         name: 'Conservation Carousel',
         scheduleItemKind: 'attractions',
      },
      {
         name: 'Kids Zoo',
         scheduleItemKind: 'attractions',
      },
   ];

   assert.deepEqual(
      filterScheduleItemRowsExcludingScheduledOccurrences(rows, {
         animals: [{ species: 'Tiger', exhibit: 'Savanna', start_time: '1:00 PM' }],
         attractions: [{ name: 'Conservation Carousel', start_time: '11:00 AM' }],
         guardiansTalks: [{ name: 'Amur Tiger', start_time: '1:30 PM' }],
         wildEncounters: [{ name: 'African Rainforest', start_time: '2:00 PM' }],
      }),
      [
         {
            name: 'Polar Bear',
            start_time: '2:00 PM',
            scheduleItemKind: 'guardians_talks',
         },
         {
            species: 'Giant Panda',
            exhibit: 'Bamboo',
            scheduleItemKind: 'animals',
         },
         {
            name: 'Kids Zoo',
            scheduleItemKind: 'attractions',
         },
      ]
   );
});

test('filterScheduleItemRowsForScheduleModule applies module-specific occurrence rules', () => {
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
         name: 'Amur Tiger',
         start_time: '1:30 PM',
         scheduleItemKind: 'guardians_talks',
      },
      {
         name: 'African Rainforest',
         start_time: '2:00 PM',
         scheduleItemKind: 'wild_encounters',
      },
   ];
   const itinerary = {
      animals: [
         { species: 'Tiger', exhibit: 'Savanna', start_time: '1:00 PM' },
         { species: 'Giant Panda', exhibit: 'Bamboo' },
      ],
      guardiansTalks: [{ name: 'Amur Tiger', start_time: '1:30 PM' }],
      wildEncounters: [{ name: 'African Rainforest', start_time: '2:00 PM' }],
   };

   assert.deepEqual(
      filterScheduleItemRowsForScheduleModule(rows, itinerary),
      [
         {
            species: 'Giant Panda',
            exhibit: 'Bamboo',
            scheduleItemKind: 'animals',
         },
      ]
   );
   assert.deepEqual(
      filterScheduleItemRowsForScheduleModule(rows, itinerary, {
         onlyItineraryItemsEnabled: true,
      }),
      [
         {
            species: 'Giant Panda',
            exhibit: 'Bamboo',
            scheduleItemKind: 'animals',
         },
      ]
   );
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
         start_time: '1:30 PM',
         scheduleItemKind: 'guardians_talks',
      },
      {
         name: 'Polar Bear',
         start_time: '2:00 PM',
         scheduleItemKind: 'guardians_talks',
      },
      {
         name: 'African Rainforest',
         start_time: '2:00 PM',
         scheduleItemKind: 'wild_encounters',
      },
   ];

   assert.deepEqual(
      filterScheduleItemRowsToItinerary(rows, {
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
         attractions: [{ name: 'Carousel' }],
         guardiansTalks: [{ name: 'Amur Tiger', start_time: '1:30 PM' }],
         wildEncounters: [{ name: 'African Rainforest', start_time: '2:00 PM' }],
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
            start_time: '1:30 PM',
            scheduleItemKind: 'guardians_talks',
         },
         {
            name: 'African Rainforest',
            start_time: '2:00 PM',
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
      start_time: '1:30 PM',
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
   assert.equal(getScheduleItemRowId(guardiansTalkRow), 'Amur Tiger||1:30 PM');
   assert.equal(tagScheduleItemRow(ScheduleItemKind.ANIMAL.itemType, null), null);
});
