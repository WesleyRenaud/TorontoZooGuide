import test from 'node:test';
import assert from 'node:assert/strict';

import { ScheduleItemSearcher } from '../../../../scripts/itinerary/panel/scheduleItemSearcher.js';
import { ScheduleItemTypes } from '../../../../scripts/itinerary/panel/scheduleItemTypes.js';
import { ItineraryEventTypes } from '../../../../scripts/itinerary/itineraryEventTypes.js';
import { GuardiansTalkScheduleItemKey } from '../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { WildEncounterScheduleItemKey } from '../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { ScheduleItemKind } from '../../../../scripts/shared/enums/scheduleItemKind.js';
import { Strings } from '../../../../scripts/strings.js';
import { TransportationScheduleItemKey } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationScheduleItemKey.js';

test('Test_BuildScheduleItemSearchPayload_TestAnimalModule_ExpectAnimalsOnly', () => {
   const query = 'panda';
   const itemType = ScheduleItemKind.ANIMAL.itemType;

   const payload = ScheduleItemSearcher.buildScheduleItemSearchPayload(itemType, query);

   assert.deepEqual(payload, {
      query,
      includeAnimals: true,
      includeOffDisplayAnimals: true,
      forItinerary: true,
   });
});


test('Test_BuildScheduleItemSearchPayload_TestAttractionModule_ExpectAttractionsOnly', () => {
   const query = 'ride';
   const itemType = ScheduleItemKind.ATTRACTION.itemType;

   const payload = ScheduleItemSearcher.buildScheduleItemSearchPayload(itemType, query);

   assert.deepEqual(payload, {
      query,
      includeAttractions: true,
      includeClosedAttractions: true,
   });
});


test('Test_BuildScheduleItemSearchPayload_TestTransportationModule_ExpectTransportationsOnly', () => {
   const query = 'zoomobile';
   const itemType = ScheduleItemKind.TRANSPORTATION.itemType;

   const payload = ScheduleItemSearcher.buildScheduleItemSearchPayload(itemType, query);

   assert.deepEqual(payload, {
      query,
      includeTransportations: true,
   });
});


test('Test_BuildScheduleItemSearchPayload_TestWildEncounterModule_ExpectWildEncountersOnly', () => {
   const query = 'rainforest';
   const itemType = ScheduleItemKind.WILD_ENCOUNTER.itemType;

   const payload = ScheduleItemSearcher.buildScheduleItemSearchPayload(itemType, query);

   assert.deepEqual(payload, {
      query,
      includeWildEncounters: true,
   });
});


test('Test_BuildScheduleItemSearchPayload_TestGuardiansTalkModule_ExpectGuardiansTalksOnly', () => {
   const query = 'tiger';
   const itemType = ScheduleItemKind.GUARDIANS_TALK.itemType;

   const payload = ScheduleItemSearcher.buildScheduleItemSearchPayload(itemType, query);

   assert.deepEqual(payload, {
      query,
      includeGuardiansTalks: true,
   });
});


test('Test_BuildSchedulableEventTypes_TestArrivalDeparture_ExpectOmitted', () => {
   const lunch = 'lunch';
   const breakType = 'break';
   const itineraryConfig = {
      eventTypes: ['arrival', lunch, 'departure', breakType],
      visitBoundaryEventTypes: {
         arrival: 'arrival',
         departure: 'departure',
      },
   };

   const eventTypes = ItineraryEventTypes.buildSchedulableEventTypes(itineraryConfig);

   assert.deepEqual(eventTypes, [lunch, breakType]);
});


test('Test_BuildSchedulableEventTypes_TestNullConfig_ExpectEmpty', () => {
   const eventTypes = ItineraryEventTypes.buildSchedulableEventTypes(null);

   assert.deepEqual(eventTypes, []);
});


test('Test_BuildScheduleItemSearchPayload_TestEventTypeSelection_ExpectQueryOnly', () => {
   const itemType = 'lunch';
   const query = 'snack';

   const payload = ScheduleItemSearcher.buildScheduleItemSearchPayload(itemType, query);

   assert.deepEqual(payload, { query });
});


test('Test_ExtractScheduleItemSearchRows_TestEventTypeSelection_ExpectEmptyRows', () => {
   const itemType = 'lunch';
   const response = {
      animals: [{ species: 'Amur Tiger', exhibit: 'Eurasia Wilds' }],
      attractions: [{ name: 'Conservation Carousel' }],
   };

   const rows = ScheduleItemSearcher.extractScheduleItemSearchRows(itemType, response);

   assert.deepEqual(rows, []);
});


test('Test_BuildScheduleItemSearchPayload_TestUnsetModule_ExpectCombinedIncludes', () => {
   const query = 'tiger';

   const payload = ScheduleItemSearcher.buildScheduleItemSearchPayload('', query);

   assert.deepEqual(payload, {
      query,
      includeAnimals: true,
      includeOffDisplayAnimals: true,
      includeAttractions: true,
      includeClosedAttractions: true,
      includeGuardiansTalks: true,
      includeWildEncounters: true,
      forItinerary: true,
   });
});


test('Test_ScheduleItemTypes_TestTypeDropdownOrder_ExpectPlaceholderFirst', () => {
   const typePlaceholder = 'Choose what to schedule';
   const breakfast = 'breakfast';
   const lunch = 'lunch';

   const options = ScheduleItemTypes.buildScheduleItemTypeOptions(
      [breakfast, lunch],
      { typePlaceholder }
   );

   assert.deepEqual(options, [
      { value: '', label: typePlaceholder, selected: true },
      { value: breakfast, label: 'Breakfast' },
      { value: lunch, label: 'Lunch' },
      { value: ScheduleItemKind.ANIMAL.itemType, label: Strings.entityLabels.animal },
      { value: ScheduleItemKind.ATTRACTION.itemType, label: Strings.entityLabels.attraction },
      {
         value: ScheduleItemKind.GUARDIANS_TALK.itemType,
         label: Strings.entityLabels.guardiansTalk,
      },
      {
         value: ScheduleItemKind.WILD_ENCOUNTER.itemType,
         label: Strings.entityLabels.wildEncounter,
      },
      {
         value: ScheduleItemKind.TRANSPORTATION.itemType,
         label: Strings.entityLabels.transportation,
      },
   ]);
});


test('Test_IsScheduleItemTypeUnset_TestEmpty_ExpectTrue', () => {
   const unset = ScheduleItemTypes.isScheduleItemTypeUnset('');

   assert.equal(unset, true);
});


test('Test_IsScheduleItemSearchEnabled_TestUnsetWithEventTypes_ExpectTrue', () => {
   const eventTypes = ['lunch', 'break'];

   const enabled = ScheduleItemTypes.isScheduleItemSearchEnabled('', eventTypes);

   assert.equal(enabled, true);
});


test('Test_IsScheduleItemEventType_TestUnset_ExpectFalse', () => {
   const eventTypes = ['lunch', 'break'];

   const isEvent = ItineraryEventTypes.isScheduleItemEventType('', eventTypes);

   assert.equal(isEvent, false);
});


test('Test_IsScheduleItemSearchEnabled_TestLunch_ExpectFalse', () => {
   const eventType = 'lunch';
   const eventTypes = [eventType, 'break'];

   const enabled = ScheduleItemTypes.isScheduleItemSearchEnabled(eventType, eventTypes);

   assert.equal(enabled, false);
});


test('Test_IsScheduleItemEventType_TestLunch_ExpectTrue', () => {
   const eventType = 'lunch';
   const eventTypes = [eventType, 'break'];

   const isEvent = ItineraryEventTypes.isScheduleItemEventType(eventType, eventTypes);

   assert.equal(isEvent, true);
});


test('Test_IsScheduleItemSearchEnabled_TestCatalogTypes_ExpectTrue', () => {
   const eventTypes = ['lunch', 'break'];
   const catalogTypes = [
      ScheduleItemKind.ANIMAL.itemType,
      ScheduleItemKind.ATTRACTION.itemType,
      ScheduleItemKind.TRANSPORTATION.itemType,
      ScheduleItemKind.GUARDIANS_TALK.itemType,
      ScheduleItemKind.WILD_ENCOUNTER.itemType,
   ];

   const enabled = catalogTypes.map((itemType) => (
      ScheduleItemTypes.isScheduleItemSearchEnabled(itemType, eventTypes)
   ));

   assert.deepEqual(enabled, catalogTypes.map(() => true));
});


test('Test_ExtractScheduleItemSearchRows_TestUnsetModule_ExpectCombinedTaggedRows', () => {
   const species = 'Giant Panda';
   const exhibit = 'Bamboo';
   const attractionName = 'Conservation Carousel';
   const talkName = 'Amur Tiger';
   const talkLocation = 'Eurasia Wilds';
   const encounterName = 'African Rainforest';
   const meetingSpot = 'Africa';
   const response = {
      animals: [{ species, exhibit }],
      attractions: [{ name: attractionName }],
      guardians_talks: [{ name: talkName, location: talkLocation }],
      wild_encounters: [{ name: encounterName, meeting_spot: meetingSpot }],
   };

   const rows = ScheduleItemSearcher.extractScheduleItemSearchRows('', response);

   assert.deepEqual(rows, [
      {
         species,
         exhibit,
         scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
      },
      {
         name: attractionName,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      },
      {
         name: talkName,
         location: talkLocation,
         scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType,
      },
      {
         name: encounterName,
         meeting_spot: meetingSpot,
         scheduleItemKind: ScheduleItemKind.WILD_ENCOUNTER.itemType,
      },
   ]);
});


test('Test_ExtractScheduleItemSearchRows_TestAnimalModule_ExpectTaggedAnimals', () => {
   const species = 'Giant Panda';
   const exhibit = 'Bamboo';
   const response = {
      animals: [{ species, exhibit }],
      attractions: [{ name: 'Conservation Carousel' }],
   };

   const rows = ScheduleItemSearcher.extractScheduleItemSearchRows(
      ScheduleItemKind.ANIMAL.itemType,
      response
   );

   assert.deepEqual(rows, [{
      species,
      exhibit,
      scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
   }]);
});


test('Test_ExtractScheduleItemSearchRows_TestAttractionModule_ExpectTaggedAttractions', () => {
   const attractionName = 'Conservation Carousel';
   const response = {
      animals: [{ species: 'Giant Panda', exhibit: 'Bamboo' }],
      attractions: [{ name: attractionName }],
   };

   const rows = ScheduleItemSearcher.extractScheduleItemSearchRows(
      ScheduleItemKind.ATTRACTION.itemType,
      response
   );

   assert.deepEqual(rows, [{
      name: attractionName,
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
   }]);
});


test('Test_ExtractScheduleItemSearchRows_TestTransportationModule_ExpectTagged', () => {
   const transportationName = 'Zoomobile';
   const attractionName = 'Conservation Carousel';
   const response = {
      transportations: [
         { name: transportationName, free_with_admission: false },
      ],
      attractions: [
         { name: attractionName, is_also_transportation: false },
         { name: transportationName, is_also_transportation: true },
      ],
   };

   const transportationRows = ScheduleItemSearcher.extractScheduleItemSearchRows(
      ScheduleItemKind.TRANSPORTATION.itemType,
      response
   );

   assert.deepEqual(transportationRows, [{
      name: transportationName,
      free_with_admission: false,
      scheduleItemKind: ScheduleItemKind.TRANSPORTATION.itemType,
   }]);
});


test('Test_ExtractScheduleItemSearchRows_TestAttractionAlsoTransportation_ExpectTagged', () => {
   const transportationName = 'Zoomobile';
   const attractionName = 'Conservation Carousel';
   const response = {
      transportations: [
         { name: transportationName, free_with_admission: false },
      ],
      attractions: [
         { name: attractionName, is_also_transportation: false },
         { name: transportationName, is_also_transportation: true },
      ],
   };

   const attractionRows = ScheduleItemSearcher.extractScheduleItemSearchRows(
      ScheduleItemKind.ATTRACTION.itemType,
      response
   );

   assert.deepEqual(attractionRows, [
      {
         name: attractionName,
         is_also_transportation: false,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      },
      {
         name: transportationName,
         is_also_transportation: true,
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      },
   ]);
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

   assert.equal(ScheduleItemSearcher.getScheduleItemRowKind(animalRow), 'animals');
   assert.equal(ScheduleItemSearcher.getScheduleItemRowKind(attractionRow), 'attractions');
   assert.equal(ScheduleItemSearcher.getScheduleItemRowKind(transportationRow), 'transportations');
   assert.equal(ScheduleItemSearcher.getScheduleItemRowKind(guardiansTalkRow), 'guardians_talks');
   assert.equal(ScheduleItemSearcher.getScheduleItemRowKind(wildEncounterRow), 'wild_encounters');
   assert.equal(ScheduleItemSearcher.getScheduleItemRowId(animalRow), 'Tiger||Savanna');
   assert.equal(ScheduleItemSearcher.getScheduleItemRowId(attractionRow), 'Carousel');
   assert.equal(ScheduleItemSearcher.getScheduleItemRowId(transportationRow), new TransportationScheduleItemKey('Zoomobile', false).toWire());
   assert.equal(
      ScheduleItemSearcher.getScheduleItemRowId(guardiansTalkRow),
      GuardiansTalkScheduleItemKey.fromRow(guardiansTalkRow).toWire()
   );
   assert.equal(
      ScheduleItemSearcher.getScheduleItemRowId(wildEncounterRow),
      WildEncounterScheduleItemKey.fromRow(wildEncounterRow).toWire()
   );
});


test('Test_ResolveEffectiveScheduleItemSelection_TestUnsetWithAnimalRow_ExpectAnimal', () => {
   const animalRow = {
      species: 'Pygmy Hippopotamus',
      exhibit: 'African Rainforest Pavilion',
      scheduleItemKind: 'animals',
   };

   assert.equal(
      ScheduleItemSearcher.resolveEffectiveScheduleItemSelection('', animalRow),
      ScheduleItemKind.ANIMAL.itemType
   );
   assert.equal(
      ScheduleItemSearcher.resolveEffectiveScheduleItemSelection(
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
      ScheduleItemSearcher.resolveEffectiveScheduleItemSelection('', transportationRow),
      ScheduleItemKind.TRANSPORTATION.itemType
   );
});


test('Test_BuildItineraryScheduleItemRowIds_TestMixedItinerary_ExpectIdSets', () => {
   const ids = ScheduleItemSearcher.buildItineraryScheduleItemRowIds({
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
   assert.equal(
      ids.guardiansTalkIds.has(
         new GuardiansTalkScheduleItemKey('Amur Tiger', '1:30 PM').toWire()
      ),
      true
   );
   assert.equal(ids.wildEncounterIds.has('African Rainforest'), false);
   assert.equal(
      ids.wildEncounterIds.has(
         new WildEncounterScheduleItemKey('Americas', '2:00 PM').toWire()
      ),
      true
   );
});


test('Test_BuildItineraryScheduleItemRowIds_TestUnscheduledOnly_ExpectUnscheduledIds', () => {
   const ids = ScheduleItemSearcher.buildItineraryScheduleItemRowIds({
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
   assert.equal(
      ids.guardiansTalkIds.has(
         new GuardiansTalkScheduleItemKey('Amur Tiger', '1:30 PM').toWire()
      ),
      false
   );
   assert.equal(ids.guardiansTalkIds.has(''), true);
});


test('Test_BuildItineraryScheduleItemRowIds_TestScheduledOnly_ExpectScheduledIds', () => {
   const ids = ScheduleItemSearcher.buildItineraryScheduleItemRowIds({
      guardiansTalks: [
         { name: 'Amur Tiger', start_time: '1:30 PM' },
         { name: 'Polar Bear', start_time: '' },
      ],
      wildEncounters: [
         { name: 'African Rainforest', start_time: '2:00 PM' },
      ],
   }, { scheduledOnly: true });

   assert.equal(
      ids.guardiansTalkIds.has(
         new GuardiansTalkScheduleItemKey('Amur Tiger', '1:30 PM').toWire()
      ),
      true
   );
   assert.equal(ids.guardiansTalkIds.has(''), false);
   assert.equal(
      ids.wildEncounterIds.has(
         new WildEncounterScheduleItemKey('African Rainforest', '2:00 PM').toWire()
      ),
      true
   );
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
      ScheduleItemSearcher.filterScheduleItemRowsExcludingScheduledOccurrences(rows, {
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
      ScheduleItemSearcher.filterScheduleItemRowsForScheduleModule(rows, itinerary),
      [
         {
            species: 'Giant Panda',
            exhibit: 'Bamboo',
            scheduleItemKind: 'animals',
         },
      ]
   );
   assert.deepEqual(
      ScheduleItemSearcher.filterScheduleItemRowsForScheduleModule(rows, itinerary, {
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
      ScheduleItemSearcher.filterScheduleItemRowsToItinerary(rows, {
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
      ScheduleItemSearcher.filterScheduleItemRowsToItinerary(
         [zoomobileAsAttractionRow, zoomobileAsTransportationRow, carouselRow],
         attractionItinerary
      ),
      [zoomobileAsAttractionRow]
   );
   assert.deepEqual(
      ScheduleItemSearcher.filterScheduleItemRowsToItinerary(
         [zoomobileAsAttractionRow, zoomobileAsTransportationRow, carouselRow],
         transportationItinerary
      ),
      [zoomobileAsTransportationRow]
   );
   assert.deepEqual(
      ScheduleItemSearcher.filterScheduleItemRowsExcludingScheduledOccurrences(
         [zoomobileAsAttractionRow, zoomobileAsTransportationRow, carouselRow],
         scheduledAttractionItinerary
      ),
      [zoomobileAsTransportationRow, carouselRow]
   );
   assert.deepEqual(
      ScheduleItemSearcher.filterScheduleItemRowsForScheduleModule(
         [zoomobileAsAttractionRow, zoomobileAsTransportationRow, carouselRow],
         attractionItinerary,
         { onlyItineraryItemsEnabled: true }
      ),
      [zoomobileAsAttractionRow]
   );
});


test('Test_TagScheduleItemRow_TestModuleKinds_ExpectTagged', () => {
   const animalRow = ScheduleItemSearcher.tagScheduleItemRow(ScheduleItemKind.ANIMAL.itemType, {
      species: 'Giant Panda',
      exhibit: 'Eurasia Wilds',
   });
   const attractionRow = ScheduleItemSearcher.tagScheduleItemRow(ScheduleItemKind.ATTRACTION.itemType, {
      name: 'Conservation Carousel',
   });
   const transportationAsAttractionRow = ScheduleItemSearcher.tagScheduleItemRow(
      ScheduleItemKind.TRANSPORTATION.itemType,
      {
         name: 'Zoomobile',
         added_as_attraction: true,
      }
   );
   const transportationRow = ScheduleItemSearcher.tagScheduleItemRow(ScheduleItemKind.TRANSPORTATION.itemType, {
      name: 'Zoomobile',
      added_as_attraction: false,
   });
   const guardiansTalkRow = ScheduleItemSearcher.tagScheduleItemRow(ScheduleItemKind.GUARDIANS_TALK.itemType, {
      name: 'Amur Tiger',
      start_time: '1:30 PM',
   });

   assert.equal(animalRow.scheduleItemKind, ScheduleItemKind.ANIMAL.itemType);
   assert.equal(
      ScheduleItemSearcher.getScheduleItemRowId(animalRow),
      'Giant Panda||Eurasia Wilds'
   );
   assert.equal(attractionRow.scheduleItemKind, ScheduleItemKind.ATTRACTION.itemType);
   assert.equal(ScheduleItemSearcher.getScheduleItemRowId(attractionRow), 'Conservation Carousel');
   assert.equal(
      transportationAsAttractionRow.scheduleItemKind,
      ScheduleItemKind.ATTRACTION.itemType
   );
   assert.equal(ScheduleItemSearcher.getScheduleItemRowId(transportationAsAttractionRow), 'Zoomobile');
   assert.equal(
      transportationRow.scheduleItemKind,
      ScheduleItemKind.TRANSPORTATION.itemType
   );
   assert.equal(ScheduleItemSearcher.getScheduleItemRowId(transportationRow), new TransportationScheduleItemKey('Zoomobile', false).toWire());
   assert.equal(
      guardiansTalkRow.scheduleItemKind,
      ScheduleItemKind.GUARDIANS_TALK.itemType
   );
   assert.equal(
      ScheduleItemSearcher.getScheduleItemRowId(guardiansTalkRow),
      GuardiansTalkScheduleItemKey.fromRow(guardiansTalkRow).toWire()
   );
   assert.equal(ScheduleItemSearcher.tagScheduleItemRow(ScheduleItemKind.ANIMAL.itemType, null), null);
});


test('Test_ResolveEffectiveScheduleItemSelection_TestUnsetWithoutRow_ExpectSelection', () => {

   assert.equal(ScheduleItemSearcher.resolveEffectiveScheduleItemSelection('', null), '');
   assert.equal(ScheduleItemSearcher.resolveEffectiveScheduleItemSelection('', undefined), '');
});


test('Test_TagScheduleItemRow_TestWildEncounter_ExpectTagged', () => {
   const wildEncounterRow = ScheduleItemSearcher.tagScheduleItemRow(
      ScheduleItemKind.WILD_ENCOUNTER.itemType,
      { name: 'African Rainforest', meeting_spot: 'Africa', start_time: '2:00 PM' }
   );

   assert.equal(wildEncounterRow.scheduleItemKind, ScheduleItemKind.WILD_ENCOUNTER.itemType);
});


test('Test_GetItineraryItemKey_TestModuleKinds_ExpectKeys', () => {

   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey(
         ScheduleItemKind.ANIMAL.itemType,
         { species: 'Tiger', exhibit: 'Savanna' }
      ),
      'Tiger||Savanna'
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey(
         ScheduleItemKind.ATTRACTION.itemType,
         { name: 'Carousel' }
      ),
      'Carousel'
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey(
         ScheduleItemKind.TRANSPORTATION.itemType,
         { name: 'Zoomobile', added_as_attraction: false }
      ),
      new TransportationScheduleItemKey('Zoomobile', false).toWire()
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey(
         ScheduleItemKind.GUARDIANS_TALK.itemType,
         { name: 'Amur Tiger', start_time: '1:30 PM' }
      ),
      new GuardiansTalkScheduleItemKey('Amur Tiger', '1:30 PM').toWire()
   );
   assert.equal(
      ScheduleItemSearcher.getItineraryItemKey(
         ScheduleItemKind.WILD_ENCOUNTER.itemType,
         { name: 'African Rainforest', start_time: '2:00 PM' }
      ).toWire(),
      new WildEncounterScheduleItemKey('African Rainforest', '2:00 PM').toWire()
   );
   assert.equal(ScheduleItemSearcher.getItineraryItemKey('', { name: 'x' }), '');
});


test('Test_ExtractScheduleItemSearchRows_TestGuardiansAndWild_ExpectTagged', () => {

   assert.deepEqual(
      ScheduleItemSearcher.extractScheduleItemSearchRows(
         ScheduleItemKind.GUARDIANS_TALK.itemType,
         { guardians_talks: [{ name: 'Tiger Talk', location: 'Eurasia' }] }
      ),
      [{
         name: 'Tiger Talk',
         location: 'Eurasia',
         scheduleItemKind: ScheduleItemKind.GUARDIANS_TALK.itemType,
      }]
   );
   assert.deepEqual(
      ScheduleItemSearcher.extractScheduleItemSearchRows(
         ScheduleItemKind.WILD_ENCOUNTER.itemType,
         { wild_encounters: [{ name: 'Rainforest', meeting_spot: 'Africa' }] }
      ),
      [{
         name: 'Rainforest',
         meeting_spot: 'Africa',
         scheduleItemKind: ScheduleItemKind.WILD_ENCOUNTER.itemType,
      }]
   );
});


test('Test_FilterScheduleItemRowsExcludingScheduledOccurrences_TestUnknownKind_ExpectKept', () => {
   const originalKind = ScheduleItemSearcher.getScheduleItemRowKind;
   ScheduleItemSearcher.getScheduleItemRowKind = () => 'unknown';

   try {

      assert.deepEqual(
         ScheduleItemSearcher.filterScheduleItemRowsExcludingScheduledOccurrences(
            [{ name: 'Mystery' }],
            {}
         ),
         [{ name: 'Mystery' }]
      );
   } finally {
      ScheduleItemSearcher.getScheduleItemRowKind = originalKind;
   }
});
