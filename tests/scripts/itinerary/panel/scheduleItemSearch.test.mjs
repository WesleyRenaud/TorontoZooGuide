import test from 'node:test';
import assert from 'node:assert/strict';

import { ScheduleItemSearch } from '../../../../scripts/itinerary/panel/scheduleItemSearch.js';
import { ScheduleItemTypes } from '../../../../scripts/itinerary/panel/scheduleItemTypes.js';
import { ItineraryEventTypes } from '../../../../scripts/itinerary/itineraryEventTypes.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { APP_STRINGS } from '../../../../scripts/strings.js';

test('Test_BuildScheduleItemSearchPayload_TestAnimalModule_ExpectAnimalsOnly', () => {
   assert.deepEqual(
      ScheduleItemSearch.buildScheduleItemSearchPayload(ScheduleItemKind.ANIMAL.itemType, 'panda'),
      {
         query: 'panda',
         includeAnimals: true,
         forItinerary: true,
      }
   );
});

test('Test_BuildScheduleItemSearchPayload_TestAttractionModule_ExpectAttractionsOnly', () => {
   assert.deepEqual(
      ScheduleItemSearch.buildScheduleItemSearchPayload(ScheduleItemKind.ATTRACTION.itemType, 'ride'),
      {
         query: 'ride',
         includeAttractions: true,
      }
   );
});

test('Test_BuildScheduleItemSearchPayload_TestTransportationModule_ExpectTransportationsOnly', () => {
   assert.deepEqual(
      ScheduleItemSearch.buildScheduleItemSearchPayload(ScheduleItemKind.TRANSPORTATION.itemType, 'zoomobile'),
      {
         query: 'zoomobile',
         includeTransportations: true,
      }
   );
});

test('Test_BuildScheduleItemSearchPayload_TestWildEncounterModule_ExpectWildEncountersOnly', () => {
   assert.deepEqual(
      ScheduleItemSearch.buildScheduleItemSearchPayload(ScheduleItemKind.WILD_ENCOUNTER.itemType, 'rainforest'),
      {
         query: 'rainforest',
         includeWildEncounters: true,
      }
   );
});

test('Test_BuildScheduleItemSearchPayload_TestGuardiansTalkModule_ExpectGuardiansTalksOnly', () => {
   assert.deepEqual(
      ScheduleItemSearch.buildScheduleItemSearchPayload(ScheduleItemKind.GUARDIANS_TALK.itemType, 'tiger'),
      {
         query: 'tiger',
         includeGuardiansTalks: true,
      }
   );
});

test('Test_BuildSchedulableEventTypes_TestArrivalDeparture_ExpectOmitted', () => {
   assert.deepEqual(
      ItineraryEventTypes.buildSchedulableEventTypes({
         eventTypes: ['arrival', 'lunch', 'departure', 'break'],
         visitBoundaryEventTypes: {
            arrival: 'arrival',
            departure: 'departure',
         },
      }),
      ['lunch', 'break']
   );
   assert.deepEqual(ItineraryEventTypes.buildSchedulableEventTypes(null), []);
});

test('Test_BuildScheduleItemSearchPayload_TestEventTypeSelection_ExpectNoCatalogSearch', () => {
   assert.deepEqual(ScheduleItemSearch.buildScheduleItemSearchPayload('lunch', 'snack'), {
      query: 'snack',
   });
   assert.deepEqual(
      ScheduleItemSearch.extractScheduleItemSearchRows('lunch', {
         animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
         attractions: [{ name: 'Carousel' }],
      }),
      []
   );
});

test('Test_BuildScheduleItemSearchPayload_TestUnsetModule_ExpectCombinedIncludes', () => {
   assert.deepEqual(ScheduleItemSearch.buildScheduleItemSearchPayload('', 'tiger'), {
      query: 'tiger',
      includeAnimals: true,
      includeAttractions: true,
      includeGuardiansTalks: true,
      includeWildEncounters: true,
      forItinerary: true,
   });
});

test('Test_ScheduleItemTypes_TestTypeDropdownOrder_ExpectPlaceholderFirst', () => {
   const options = ScheduleItemTypes.buildScheduleItemTypeOptions(
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
         value: 'transportations',
         label: APP_STRINGS.entityLabels.transportation,
      },
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

test('Test_ScheduleItemTypes_TestPlaceholderAndEventTypes_ExpectSearchFlags', () => {
   const eventTypes = ['lunch', 'break'];

   assert.equal(ScheduleItemTypes.isScheduleItemTypeUnset(''), true);
   assert.equal(ScheduleItemTypes.isScheduleItemSearchEnabled('', eventTypes), true);
   assert.equal(ItineraryEventTypes.isScheduleItemEventType('', eventTypes), false);
   assert.equal(ScheduleItemTypes.isScheduleItemSearchEnabled('lunch', eventTypes), false);
   assert.equal(ItineraryEventTypes.isScheduleItemEventType('lunch', eventTypes), true);
   assert.equal(
      ScheduleItemTypes.isScheduleItemSearchEnabled(ScheduleItemKind.ANIMAL.itemType, eventTypes),
      true
   );
   assert.equal(
      ScheduleItemTypes.isScheduleItemSearchEnabled(ScheduleItemKind.ATTRACTION.itemType, eventTypes),
      true
   );
   assert.equal(
      ScheduleItemTypes.isScheduleItemSearchEnabled(ScheduleItemKind.TRANSPORTATION.itemType, eventTypes),
      true
   );
   assert.equal(
      ScheduleItemTypes.isScheduleItemSearchEnabled(ScheduleItemKind.GUARDIANS_TALK.itemType, eventTypes),
      true
   );
   assert.equal(
      ScheduleItemTypes.isScheduleItemSearchEnabled(ScheduleItemKind.WILD_ENCOUNTER.itemType, eventTypes),
      true
   );
});

test('Test_ExtractScheduleItemSearchRows_TestUnsetModule_ExpectCombinedTaggedRows', () => {
   const response = {
      animals: [{ species: 'Giant Panda', exhibit: 'Bamboo' }],
      attractions: [{ name: 'Carousel' }],
      guardians_talks: [{ name: 'Amur Tiger', location: 'Eurasia Wilds' }],
      wild_encounters: [{ name: 'African Rainforest', meeting_spot: 'Africa' }],
   };

   assert.deepEqual(
      ScheduleItemSearch.extractScheduleItemSearchRows('', response),
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

test('Test_ExtractScheduleItemSearchRows_TestSelectedModule_ExpectTaggedCollection', () => {
   const response = {
      animals: [{ species: 'Giant Panda', exhibit: 'Bamboo' }],
      attractions: [{ name: 'Carousel' }],
   };

   assert.deepEqual(
      ScheduleItemSearch.extractScheduleItemSearchRows(ScheduleItemKind.ANIMAL.itemType, response),
      [{
         species: 'Giant Panda',
         exhibit: 'Bamboo',
         scheduleItemKind: 'animals',
      }]
   );
   assert.deepEqual(
      ScheduleItemSearch.extractScheduleItemSearchRows(ScheduleItemKind.ATTRACTION.itemType, response),
      [{
         name: 'Carousel',
         scheduleItemKind: 'attractions',
      }]
   );
});

test('Test_ExtractScheduleItemSearchRows_TestTransportationModule_ExpectTagged', () => {
   const response = {
      transportations: [
         { name: 'Zoomobile', free_with_admission: false },
      ],
      attractions: [
         { name: 'Carousel', is_also_transportation: false },
         { name: 'Zoomobile', is_also_transportation: true },
      ],
   };

   assert.deepEqual(
      ScheduleItemSearch.extractScheduleItemSearchRows(ScheduleItemKind.TRANSPORTATION.itemType, response),
      [{
         name: 'Zoomobile',
         free_with_admission: false,
         scheduleItemKind: 'transportations',
      }]
   );
   assert.deepEqual(
      ScheduleItemSearch.extractScheduleItemSearchRows(ScheduleItemKind.ATTRACTION.itemType, response),
      [
         {
            name: 'Carousel',
            is_also_transportation: false,
            scheduleItemKind: 'attractions',
         },
         {
            name: 'Zoomobile',
            is_also_transportation: true,
            scheduleItemKind: 'attractions',
         },
      ]
   );
});

test('Test_GetScheduleItemRowKindAndId_TestMixedRows_ExpectResolved', () => {
   const animalRow = {
      species: 'Tiger',
      exhibit: 'Savanna',
      scheduleItemKind: 'animals',
   };
   const attractionRow = {
      name: 'Carousel',
      scheduleItemKind: 'attractions',
   };
   const transportationRow = {
      name: 'Zoomobile',
      added_as_attraction: false,
      scheduleItemKind: 'transportations',
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

   assert.equal(ScheduleItemSearch.getScheduleItemRowKind(animalRow), 'animals');
   assert.equal(ScheduleItemSearch.getScheduleItemRowKind(attractionRow), 'attractions');
   assert.equal(ScheduleItemSearch.getScheduleItemRowKind(transportationRow), 'transportations');
   assert.equal(ScheduleItemSearch.getScheduleItemRowKind(guardiansTalkRow), 'guardians_talks');
   assert.equal(ScheduleItemSearch.getScheduleItemRowKind(wildEncounterRow), 'wild_encounters');
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(animalRow), 'Tiger||Savanna');
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(attractionRow), 'Carousel');
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(transportationRow), 'Zoomobile||0');
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(guardiansTalkRow), 'Amur Tiger||14:00');
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(wildEncounterRow), 'African Rainforest||14:00');
});

test('Test_ResolveEffectiveScheduleItemSelection_TestUnsetWithAnimalRow_ExpectAnimal', () => {
   const animalRow = {
      species: 'Pygmy Hippopotamus',
      exhibit: 'African Rainforest Pavilion',
      scheduleItemKind: 'animals',
   };

   assert.equal(
      ScheduleItemSearch.resolveEffectiveScheduleItemSelection('', animalRow),
      ScheduleItemKind.ANIMAL.itemType
   );
   assert.equal(
      ScheduleItemSearch.resolveEffectiveScheduleItemSelection(
         ScheduleItemKind.ATTRACTION.itemType,
         animalRow
      ),
      ScheduleItemKind.ATTRACTION.itemType
   );
});

test('Test_ResolveEffectiveScheduleItemSelection_TestUnsetWithTransportationRow_ExpectTransportation', () => {
   const transportationRow = {
      name: 'Zoomobile',
      added_as_attraction: false,
      scheduleItemKind: 'transportations',
   };

   assert.equal(
      ScheduleItemSearch.resolveEffectiveScheduleItemSelection('', transportationRow),
      ScheduleItemKind.TRANSPORTATION.itemType
   );
});

test('Test_BuildItineraryScheduleItemRowIds_TestMixedItinerary_ExpectIdSets', () => {
   const ids = ScheduleItemSearch.buildItineraryScheduleItemRowIds({
      animals: [{ species: 'Tiger', exhibit: 'Savanna' }],
      attractions: [{ name: 'Carousel' }],
      transportations: [
         { name: 'Zoomobile', added_as_attraction: true },
         { name: 'Zoo Shuttle', added_as_attraction: false },
      ],
      guardiansTalks: [{ name: 'Amur Tiger', start_time: '1:30 PM' }],
      wildEncounters: [
         { name: 'African Rainforest', start_time: '' },
         { name: 'Americas', start_time: '2:00 PM' },
      ],
   });

   assert.equal(ids.animalIds.has('Tiger||Savanna'), true);
   assert.equal(ids.attractionIds.has('Carousel'), true);
   assert.equal(ids.attractionIds.has('Zoomobile'), true);
   assert.equal(ids.attractionIds.has('Zoo Shuttle'), false);
   assert.equal(ids.transportationIds.has('Zoomobile'), false);
   assert.equal(ids.transportationIds.has('Zoo Shuttle'), false);
   assert.equal(ids.transportationIds.has('Zoo Shuttle||0'), true);
   assert.equal(ids.guardiansTalkIds.has('Amur Tiger||1:30 PM'), true);
   assert.equal(ids.wildEncounterIds.has('African Rainforest'), false);
   assert.equal(ids.wildEncounterIds.has('Americas||2:00 PM'), true);
});

test('Test_BuildItineraryScheduleItemRowIds_TestUnscheduledOnly_ExpectUnscheduledIds', () => {
   const ids = ScheduleItemSearch.buildItineraryScheduleItemRowIds({
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

test('Test_BuildItineraryScheduleItemRowIds_TestScheduledOnly_ExpectScheduledIds', () => {
   const ids = ScheduleItemSearch.buildItineraryScheduleItemRowIds({
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

test('Test_FilterScheduleItemRowsExcludingScheduledOccurrences_TestScheduledItems_ExpectHidden', () => {
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
      ScheduleItemSearch.filterScheduleItemRowsExcludingScheduledOccurrences(rows, {
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

test('Test_FilterScheduleItemRowsForScheduleModule_TestOccurrenceRules_ExpectFiltered', () => {
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
      ScheduleItemSearch.filterScheduleItemRowsForScheduleModule(rows, itinerary),
      [
         {
            species: 'Giant Panda',
            exhibit: 'Bamboo',
            scheduleItemKind: 'animals',
         },
      ]
   );
   assert.deepEqual(
      ScheduleItemSearch.filterScheduleItemRowsForScheduleModule(rows, itinerary, {
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

test('Test_FilterScheduleItemRowsToItinerary_TestOwnedRows_ExpectKept', () => {
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
      ScheduleItemSearch.filterScheduleItemRowsToItinerary(rows, {
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

test('Test_FilterScheduleItemRowsToItinerary_TestAddedAsAttraction_ExpectAttractionId', () => {
   const zoomobileAsAttractionRow = {
      name: 'Zoomobile',
      added_as_attraction: true,
      scheduleItemKind: 'attractions',
   };
   const zoomobileAsTransportationRow = {
      name: 'Zoomobile',
      added_as_attraction: false,
      scheduleItemKind: 'transportations',
   };
   const carouselRow = {
      name: 'Carousel',
      scheduleItemKind: 'attractions',
   };
   const attractionItinerary = {
      attractions: [],
      transportations: [
         { name: 'Zoomobile', added_as_attraction: true },
      ],
   };
   const transportationItinerary = {
      attractions: [],
      transportations: [
         { name: 'Zoomobile', added_as_attraction: false },
      ],
   };
   const scheduledAttractionItinerary = {
      attractions: [],
      transportations: [
         {
            name: 'Zoomobile',
            added_as_attraction: true,
            start_time: '10:00 AM',
         },
      ],
   };

   assert.deepEqual(
      ScheduleItemSearch.filterScheduleItemRowsToItinerary(
         [zoomobileAsAttractionRow, zoomobileAsTransportationRow, carouselRow],
         attractionItinerary
      ),
      [zoomobileAsAttractionRow]
   );
   assert.deepEqual(
      ScheduleItemSearch.filterScheduleItemRowsToItinerary(
         [zoomobileAsAttractionRow, zoomobileAsTransportationRow, carouselRow],
         transportationItinerary
      ),
      [zoomobileAsTransportationRow]
   );
   assert.deepEqual(
      ScheduleItemSearch.filterScheduleItemRowsExcludingScheduledOccurrences(
         [zoomobileAsAttractionRow, zoomobileAsTransportationRow, carouselRow],
         scheduledAttractionItinerary
      ),
      [zoomobileAsTransportationRow, carouselRow]
   );
   assert.deepEqual(
      ScheduleItemSearch.filterScheduleItemRowsForScheduleModule(
         [zoomobileAsAttractionRow, zoomobileAsTransportationRow, carouselRow],
         attractionItinerary,
         { onlyItineraryItemsEnabled: true }
      ),
      [zoomobileAsAttractionRow]
   );
});

test('Test_TagScheduleItemRow_TestModuleKinds_ExpectTagged', () => {
   const animalRow = ScheduleItemSearch.tagScheduleItemRow(ScheduleItemKind.ANIMAL.itemType, {
      species: 'Giant Panda',
      exhibit: 'Eurasia Wilds',
   });
   const attractionRow = ScheduleItemSearch.tagScheduleItemRow(ScheduleItemKind.ATTRACTION.itemType, {
      name: 'Conservation Carousel',
   });
   const transportationAsAttractionRow = ScheduleItemSearch.tagScheduleItemRow(
      ScheduleItemKind.TRANSPORTATION.itemType,
      {
         name: 'Zoomobile',
         added_as_attraction: true,
      }
   );
   const transportationRow = ScheduleItemSearch.tagScheduleItemRow(ScheduleItemKind.TRANSPORTATION.itemType, {
      name: 'Zoomobile',
      added_as_attraction: false,
   });
   const guardiansTalkRow = ScheduleItemSearch.tagScheduleItemRow(ScheduleItemKind.GUARDIANS_TALK.itemType, {
      name: 'Amur Tiger',
      start_time: '1:30 PM',
   });

   assert.equal(animalRow.scheduleItemKind, ScheduleItemKind.ANIMAL.itemType);
   assert.equal(
      ScheduleItemSearch.getScheduleItemRowId(animalRow),
      'Giant Panda||Eurasia Wilds'
   );
   assert.equal(attractionRow.scheduleItemKind, ScheduleItemKind.ATTRACTION.itemType);
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(attractionRow), 'Conservation Carousel');
   assert.equal(
      transportationAsAttractionRow.scheduleItemKind,
      ScheduleItemKind.ATTRACTION.itemType
   );
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(transportationAsAttractionRow), 'Zoomobile');
   assert.equal(
      transportationRow.scheduleItemKind,
      ScheduleItemKind.TRANSPORTATION.itemType
   );
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(transportationRow), 'Zoomobile||0');
   assert.equal(
      guardiansTalkRow.scheduleItemKind,
      ScheduleItemKind.GUARDIANS_TALK.itemType
   );
   assert.equal(ScheduleItemSearch.getScheduleItemRowId(guardiansTalkRow), 'Amur Tiger||1:30 PM');
   assert.equal(ScheduleItemSearch.tagScheduleItemRow(ScheduleItemKind.ANIMAL.itemType, null), null);
});
