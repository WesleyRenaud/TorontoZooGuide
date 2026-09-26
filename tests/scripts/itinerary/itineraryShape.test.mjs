import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryShape } from '../../../scripts/itinerary/itineraryShape.js';
import { WildEncounterScheduleItemKey } from '../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_CreateEmptyItineraryDraft_TestDefault_ExpectEmptyShape', () => {
   const emptyDraft = ItineraryShape.createEmptyItineraryDraft();

   assert.deepEqual(emptyDraft, {
      date: '',
      arrivalTime: '',
      departureTime: '',
      animals: [],
      attractions: [],
      guardiansTalks: [],
      wildEncounters: [],
      transportations: [],
      transportationStations: [],
      events: [],
   });
});


test('Test_NormalizeItineraryDraft_TestMixedInput_ExpectNormalizedShape', () => {
   const date = '2026-06-15';
   const arrivalTime = '09:30';
   const departureTime = '17:00';
   const animals = [{ species: 'African Lion' }];
   const guardiansTalks = [{ name: 'Amur Tiger' }];
   const draft = {
      date,
      arrivalTime,
      departureTime,
      animals,
      attractions: 'Conservation Carousel',
      guardiansTalks,
      wildEncounters: null,
   };

   const normalized = ItineraryShape.normalizeItineraryDraft(draft);

   assert.equal(normalized.date, date);
   assert.equal(normalized.arrivalTime, arrivalTime);
   assert.equal(normalized.departureTime, departureTime);
   assert.equal(normalized.animals, animals);
   assert.deepEqual(normalized.attractions, []);
   assert.equal(normalized.guardiansTalks, guardiansTalks);
   assert.deepEqual(normalized.wildEncounters, []);
   assert.deepEqual(normalized.transportations, []);
   assert.deepEqual(normalized.transportationStations, []);
   assert.deepEqual(normalized.events, []);
});


test('Test_NormalizeItineraryDraft_TestEvents_ExpectPreserved', () => {
   const event = { event_type: 'lunch', start_time: '12:00', end_time: '12:40' };

   const normalized = ItineraryShape.normalizeItineraryDraft({
      events: [event],
   });

   assert.equal(normalized.date, '');
   assert.equal(normalized.arrivalTime, '');
   assert.equal(normalized.departureTime, '');
   assert.deepEqual(normalized.animals, []);
   assert.deepEqual(normalized.attractions, []);
   assert.deepEqual(normalized.guardiansTalks, []);
   assert.deepEqual(normalized.wildEncounters, []);
   assert.deepEqual(normalized.transportations, []);
   assert.deepEqual(normalized.transportationStations, []);
   assert.deepEqual(normalized.events[Position.FIRST], event);
});


test('Test_CloneItineraryDraft_TestArrayFields_ExpectIndependentCopy', () => {
   const species = 'African Lion';
   const animals = [{ species }];
   const draft = {
      date: '2026-06-15',
      animals,
      attractions: [{ name: 'Conservation Carousel' }],
      guardiansTalks: [],
      wildEncounters: [{ name: 'African Rainforest' }],
   };

   const clone = ItineraryShape.cloneItineraryDraft(draft);
   clone.animals.push({ species: 'Amur Tiger' });

   assert.notEqual(clone.animals, draft.animals);
   assert.deepEqual(draft.animals, animals);
});


test('Test_AreItineraryDraftsEqual_TestSameAnimals_ExpectTrue', () => {
   const date = '2026-06-15';
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna', likelihood: 90 };
   const left = { date, animals: [animal] };
   const right = { date, animals: [{ ...animal }] };

   const areEqual = ItineraryShape.areItineraryDraftsEqual(left, right);

   assert.equal(areEqual, true);
});


test('Test_AreItineraryDraftsEqual_TestDifferentAnimals_ExpectFalse', () => {
   const left = { animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }] };
   const right = { animals: [{ species: 'Amur Tiger', exhibit: 'Eurasia' }] };

   const areEqual = ItineraryShape.areItineraryDraftsEqual(left, right);

   assert.equal(areEqual, false);
});


test('Test_AreItineraryDraftsSemanticallyEqual_TestMetadataDifference_ExpectEqual', () => {
   const date = '2026-06-15';
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const left = {
      date,
      animals: [
         { species, exhibit, likelihood: 90, imageSrc: '/a.png' },
      ],
   };
   const right = {
      date,
      animals: [
         { species, exhibit, likelihood: 5 },
      ],
   };

   const areEqual = ItineraryShape.areItineraryDraftsSemanticallyEqual(left, right);

   assert.equal(areEqual, true);
});


test('Test_AreItineraryDraftsSemanticallyEqual_TestOrderDifference_ExpectEqual', () => {
   const date = '2026-06-15';
   const tiger = { species: 'Amur Tiger', exhibit: 'Eurasia' };
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const left = { date, animals: [tiger, lion] };
   const right = { date, animals: [lion, tiger] };

   const areEqual = ItineraryShape.areItineraryDraftsSemanticallyEqual(left, right);

   assert.equal(areEqual, true);
});


test('Test_AreItineraryDraftsSemanticallyEqual_TestDifferentDates_ExpectNotEqual', () => {
   const animal = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const left = { date: '2026-06-15', animals: [animal] };
   const right = { date: '2026-06-16', animals: [animal] };

   const areEqual = ItineraryShape.areItineraryDraftsSemanticallyEqual(left, right);

   assert.equal(areEqual, false);
});


test('Test_IsItineraryEmptyDraft_TestDateOnly_ExpectNonEmpty', () => {
   const date = '2026-06-15';

   const isEmpty = ItineraryShape.isItineraryEmptyDraft({ date });

   assert.equal(isEmpty, false);
});


test('Test_IsItineraryEmptyDraft_TestArrivalTime_ExpectNonEmpty', () => {
   const date = '2026-06-15';
   const arrivalTime = '09:30';

   const isEmpty = ItineraryShape.isItineraryEmptyDraft({ date, arrivalTime });

   assert.equal(isEmpty, false);
});


test('Test_IsItineraryEmptyDraft_TestWildEncounters_ExpectNonEmpty', () => {
   const date = '2026-06-15';
   const wildEncounters = [{ name: 'African Rainforest' }];

   const isEmpty = ItineraryShape.isItineraryEmptyDraft({ date, wildEncounters });

   assert.equal(isEmpty, false);
});


test('Test_IsItineraryEmptyDraft_TestEvents_ExpectNonEmpty', () => {
   const date = '2026-06-15';
   const events = [{ event_type: 'lunch', start_time: '12:00', end_time: '12:40' }];

   const isEmpty = ItineraryShape.isItineraryEmptyDraft({ date, events });

   assert.equal(isEmpty, false);
});


test('Test_IsItineraryEmptyDraft_TestAddedAsAttractionTransportation_ExpectNonEmpty', () => {
   const transportations = [{ name: 'Zoomobile', added_as_attraction: true }];

   const isEmpty = ItineraryShape.isItineraryEmptyDraft({ transportations });

   assert.equal(isEmpty, false);
});


test('Test_HasSavedItineraryContent_TestDateOnly_ExpectTrue', () => {
   const date = '2026-06-15';

   const hasContent = ItineraryShape.hasSavedItineraryContent({ date });

   assert.equal(hasContent, true);
});


test('Test_IsItineraryCompletelyUnset_TestDateOnly_ExpectFalse', () => {
   const date = '2026-06-15';

   const isUnset = ItineraryShape.isItineraryCompletelyUnset({ date });

   assert.equal(isUnset, false);
});


test('Test_IsItineraryCompletelyUnset_TestNull_ExpectTrue', () => {
   const draft = null;

   const isUnset = ItineraryShape.isItineraryCompletelyUnset(draft);

   assert.equal(isUnset, true);
});


test('Test_IsItineraryCompletelyUnset_TestEmptyObject_ExpectTrue', () => {
   const draft = {};

   const isUnset = ItineraryShape.isItineraryCompletelyUnset(draft);

   assert.equal(isUnset, true);
});


test('Test_IsItineraryEmptyDraft_TestAnimals_ExpectNonEmpty', () => {
   const date = '2026-06-15';
   const animals = [{ species: 'Tiger', exhibit: 'Savanna' }];

   const isEmpty = ItineraryShape.isItineraryEmptyDraft({ date, animals });

   assert.equal(isEmpty, false);
});


test('Test_ToSetItineraryPayload_TestCanonicalShapes_ExpectSaveApiShape', () => {
   const date = '2026-06-15';
   const africanLion = 'African Lion';
   const africaSavanna = 'Africa Savanna';
   const masaiGiraffe = 'Masai Giraffe';
   const giraffeHouse = 'Giraffe House';
   const conservationCarousel = 'Conservation Carousel';
   const greenhouse = 'Greenhouse';
   const rainforest = 'African Rainforest';
   const startTime = '14:00';

   const payload = ItineraryShape.toSetItineraryPayload({
      date,
      animals: [
         { species: africanLion, exhibit: africaSavanna, likelihood: 90 },
         { species: '  ', exhibit: africaSavanna },
         {
            species: ` ${masaiGiraffe} `,
            exhibit: africaSavanna,
            enclosure_name: ` ${giraffeHouse} `,
         },
      ],
      attractions: [{ name: conservationCarousel }, greenhouse],
      guardiansTalks: [{ name: africanLion, type: 'guardiansTalk' }],
      wildEncounters: [{ name: rainforest, start_time: startTime }],
   });

   assert.equal(payload.date, date);
   assert.equal(payload.arrivalTime, '');
   assert.equal(payload.departureTime, '');
   assert.deepEqual(payload.animals, [
      { species: africanLion, exhibit: africaSavanna },
      {
         species: masaiGiraffe,
         exhibit: africaSavanna,
         enclosure_name: giraffeHouse,
      },
   ]);
   assert.deepEqual(payload.attractions, [conservationCarousel, greenhouse]);
   assert.deepEqual(payload.transportations, []);
   assert.deepEqual(payload.guardiansTalks, [{
      name: africanLion,
      start_time: null,
      end_time: null,
   }]);
   assert.deepEqual(
      payload.wildEncounters,
      [new WildEncounterScheduleItemKey(rainforest, startTime).toWire()]
   );
});


test('Test_HydrateWizardDraftFromSavedItinerary_TestAddedAsAttraction_ExpectMovedToAttractions', () => {
   const date = '2026-08-17';
   const zoomobile = 'Zoomobile';
   const zooShuttle = 'Zoo Shuttle';

   const hydrated = ItineraryShape.hydrateWizardDraftFromSavedItinerary({
      date,
      attractions: [],
      transportations: [
         { name: zoomobile, added_as_attraction: true },
         { name: zooShuttle, added_as_attraction: false },
      ],
   });

   assert.equal(hydrated.date, date);
   assert.deepEqual(hydrated.attractions, [{ name: zoomobile, addedAsAttraction: true }]);
   assert.deepEqual(hydrated.transportations, [{ name: zooShuttle, added_as_attraction: false }]);
});


test('Test_HydrateWizardDraftFromSavedItinerary_TestTransportationOnlyAnimals_ExpectStripped', () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const giraffe = {
      species: 'Masai Giraffe',
      exhibit: 'Africa Savanna',
      enclosure_name: 'Outdoor',
      added_by_transportation: true,
   };

   const hydrated = ItineraryShape.hydrateWizardDraftFromSavedItinerary({
      animals: [lion, giraffe],
   });

   assert.deepEqual(hydrated.animals, [lion]);
});


test('Test_ToSetItineraryPayload_TestTransportationOnlyAnimals_ExpectOmitted', () => {
   const lion = { species: 'African Lion', exhibit: 'Africa Savanna' };
   const giraffe = {
      species: 'Masai Giraffe',
      exhibit: 'Africa Savanna',
      enclosure_name: 'Outdoor',
      added_by_transportation: true,
   };

   const payload = ItineraryShape.toSetItineraryPayload({
      animals: [lion, giraffe],
   });

   assert.deepEqual(payload.animals, [lion]);
});


test('Test_HydrateWizardDraftFromSavedItinerary_TestBlankOrDuplicateAttractionNames_ExpectSkipped', () => {
   const zoomobile = { name: 'Zoomobile' };

   const hydrated = ItineraryShape.hydrateWizardDraftFromSavedItinerary({
      attractions: [zoomobile],
      transportations: [
         { name: ' ', added_as_attraction: true },
         { name: zoomobile.name, added_as_attraction: true },
      ],
   });

   assert.deepEqual(hydrated.attractions, [zoomobile]);
});


test('Test_ToSetItineraryPayload_TestSameNameRoles_ExpectBothKept', () => {
   const date = '2026-08-17';
   const name = 'Zoomobile';

   const payload = ItineraryShape.toSetItineraryPayload({
      date,
      attractions: [{ name, addedAsAttraction: true }],
      transportations: [{ name, addedAsAttraction: false }],
   });

   assert.deepEqual(payload.transportations, [
      { name, added_as_attraction: false },
      { name, added_as_attraction: true },
   ]);
});


test('Test_ToSetItineraryPayload_TestSavedAddedAsAttraction_ExpectPreserved', () => {
   const date = '2026-08-17';
   const name = 'Zoomobile';
   const addedAsAttraction = true;

   const payload = ItineraryShape.toSetItineraryPayload({
      date,
      animals: [{ species: 'African Lion', exhibit: 'Africa Savanna' }],
      transportations: [{ name, added_as_attraction: addedAsAttraction }],
   });

   assert.deepEqual(payload.transportations, [{
      name,
      added_as_attraction: addedAsAttraction,
   }]);
});


test('Test_ToSetItineraryPayload_TestAlsoTransportationAttractions_ExpectMoved', () => {
   const date = '2026-06-15';
   const conservationCarousel = 'Conservation Carousel';
   const zoomobile = 'Zoomobile';
   const zooShuttle = 'Zoo Shuttle';

   const payload = ItineraryShape.toSetItineraryPayload({
      date,
      attractions: [
         { name: conservationCarousel },
         { name: zoomobile, addedAsAttraction: true },
      ],
      transportations: [
         { name: zooShuttle, addedAsAttraction: false },
      ],
   });

   assert.equal(payload.date, date);
   assert.deepEqual(payload.attractions, [conservationCarousel]);
   assert.deepEqual(payload.transportations, [
      { name: zooShuttle, added_as_attraction: false },
      { name: zoomobile, added_as_attraction: true },
   ]);
});


test('Test_ToSetItineraryPayload_TestWildEncounters_ExpectWireStrings', () => {
   const date = '2026-06-15';
   const name = 'Kangaroo';
   const startTime = '13:00';
   const endTime = '13:45';

   const payload = ItineraryShape.toSetItineraryPayload({
      date,
      wildEncounters: [{
         name,
         start_time: startTime,
         end_time: endTime,
      }],
   });

   assert.deepEqual(
      payload.wildEncounters,
      [new WildEncounterScheduleItemKey(name, startTime, endTime).toWire()]
   );
});


test('Test_ToSetItineraryPayload_TestScheduleTimes_ExpectPreserved', () => {
   const date = '2026-06-15';
   const arrivalTime = '09:30';
   const departureTime = '17:00';
   const talkName = 'African Lion';
   const talkStart = '13:45';
   const talkEnd = '14:00';
   const encounterName = 'Grizzly Bear';
   const encounterStart = '13:00';

   const payload = ItineraryShape.toSetItineraryPayload({
      date,
      arrivalTime,
      departureTime,
      animals: [],
      attractions: [],
      guardiansTalks: [{
         name: talkName,
         start_time: talkStart,
         end_time: talkEnd,
      }],
      wildEncounters: [{
         name: encounterName,
         start_time: encounterStart,
      }],
   });

   assert.equal(payload.date, date);
   assert.equal(payload.arrivalTime, arrivalTime);
   assert.equal(payload.departureTime, departureTime);
   assert.deepEqual(payload.animals, []);
   assert.deepEqual(payload.attractions, []);
   assert.deepEqual(payload.transportations, []);
   assert.deepEqual(payload.guardiansTalks, [{
      name: talkName,
      start_time: talkStart,
      end_time: talkEnd,
   }]);
   assert.deepEqual(
      payload.wildEncounters,
      [new WildEncounterScheduleItemKey(encounterName, encounterStart).toWire()]
   );
});
