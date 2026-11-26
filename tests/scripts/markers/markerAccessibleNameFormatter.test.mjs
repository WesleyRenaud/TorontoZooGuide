import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerAccessibleNameFormatter } from '../../../scripts/markers/markerAccessibleNameFormatter.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Strings } from '../../../scripts/strings.js';


function _animals(count, firstSpecies = 'Black Tree Monitor') {
   return Array.from({ length: count }, (_, index) => ({
      type: ItemType.ANIMAL,
      species: index === 0 ? firstSpecies : `Other ${index}`,
   }));
}


test('Test_BuildAccessibleName_TestEmptyItems_ExpectBlank', () => {
   assert.equal(MarkerAccessibleNameFormatter.buildAccessibleName(null), '');
   assert.equal(MarkerAccessibleNameFormatter.buildAccessibleName([]), '');
});


test('Test_BuildAccessibleName_TestSingleAnimal_ExpectSpeciesName', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName(_animals(1, 'Demoiselle Crane'));

   assert.equal(name, 'Demoiselle Crane');
});


test('Test_BuildAccessibleName_TestAnimalCluster_ExpectCountThenSpecies', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName(_animals(37));

   assert.equal(
      name,
      Strings.map.markerAriaGroup(37, 'species', 'Black Tree Monitor', 36)
   );
   assert.equal(name, '37 species: Black Tree Monitor and 36 more');
   assert.equal(name.startsWith('37'), true);
});


test('Test_BuildAccessibleName_TestTwoAnimals_ExpectOneMore', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName(_animals(2, 'Amur Tiger'));

   assert.equal(name, '2 species: Amur Tiger and 1 more');
});


test('Test_BuildAccessibleName_TestSingleRestaurant_ExpectNameOnly', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.RESTAURANT, name: 'Peaks Cafe' },
   ]);

   assert.equal(name, 'Peaks Cafe');
});


test('Test_BuildAccessibleName_TestRestaurantCluster_ExpectCountThenName', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.RESTAURANT, name: 'Peaks Cafe' },
      { type: ItemType.RESTAURANT, name: 'Simba Safari Cafe' },
      { type: ItemType.RESTAURANT, name: 'Sylvans' },
   ]);

   assert.equal(name, '3 restaurants: Peaks Cafe and 2 more');
   assert.equal(name.startsWith('3'), true);
});


test('Test_BuildAccessibleName_TestHiddenType_ExpectBlank', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.TRANSPORTATION_ROUTE_MARKER },
      { type: ItemType.TRANSPORTATION_ROUTE_MARKER },
   ]);

   assert.equal(name, '');
});


test('Test_BuildAccessibleName_TestGuardiansTalkCluster_ExpectTalkNoun', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.GUARDIANS_TALK, name: 'Amur Tiger' },
      { type: ItemType.GUARDIANS_TALK, name: 'Indian Rhino' },
   ]);

   assert.equal(name, '2 talks: Amur Tiger and 1 more');
});


test('Test_BuildAccessibleName_TestSingleWildEncounter_ExpectHoverText', () => {
   const encounterName = 'Red Panda';
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.WILD_ENCOUNTER, name: encounterName },
   ]);

   assert.equal(name, Strings.map.hover.wildEncounterMeetingSpotWithName(encounterName));
});


test('Test_BuildAccessibleName_TestWildEncounterCluster_ExpectCountThenName', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.WILD_ENCOUNTER, name: 'Red Panda' },
      { type: ItemType.WILD_ENCOUNTER, name: 'Gorilla' },
   ]);

   assert.equal(name, '2 wild encounters: Red Panda and 1 more');
});


test('Test_BuildAccessibleName_TestDrinkingFountainCluster_ExpectFixedTitle', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.DRINKING_FOUNTAIN },
      { type: ItemType.DRINKING_FOUNTAIN },
   ]);

   assert.equal(
      name,
      `2 drinking fountains: ${Strings.map.hover.drinkingFountain} and 1 more`
   );
});


test('Test_BuildAccessibleName_TestOtherCountedTypes_ExpectCountAndNoun', () => {
   const cases = [
      {
         items: [
            { type: ItemType.PAVILION, name: 'African Savanna' },
            { type: ItemType.PAVILION, name: 'Australasia Pavilion' },
         ],
         expected: '2 pavilions: African Savanna and 1 more',
      },
      {
         items: [
            { type: ItemType.RESTROOM, title: 'Wheelchair Accessible' },
            { type: ItemType.RESTROOM, title: 'Standard' },
         ],
         expected: `2 ${Strings.entityLabels.restrooms}: Wheelchair Accessible and 1 more`,
      },
      {
         items: [
            { type: ItemType.GIFT_SHOP, name: 'Gift Shop' },
            { type: ItemType.GIFT_SHOP, name: 'Zoo Shop' },
         ],
         expected: `2 ${Strings.entityLabels.giftShops}: Gift Shop and 1 more`,
      },
      {
         items: [
            { type: ItemType.ATTRACTION, name: 'Splash Island' },
            { type: ItemType.ATTRACTION, name: 'Conservation Carousel' },
         ],
         expected: `2 ${Strings.entityLabels.attractions}: Splash Island and 1 more`,
      },
      {
         items: [
            { type: ItemType.TRANSPORTATION, name: 'Zoomobile' },
            { type: ItemType.TRANSPORTATION, name: 'Shuttle' },
         ],
         expected: `2 ${Strings.entityLabels.attractions}: Zoomobile and 1 more`,
      },
      {
         items: [
            { type: ItemType.TRANSPORTATION_STATION, name: 'Main Station' },
            { type: ItemType.TRANSPORTATION_STATION, name: 'African Station' },
         ],
         expected: '2 stations: Main Station and 1 more',
      },
      {
         items: [
            { type: ItemType.GUEST_SERVICE, service_type: 'Wheelchair Rental' },
            { type: ItemType.GUEST_SERVICE, service_type: 'Stroller Rental' },
         ],
         expected: '2 guest services: Wheelchair Rental and 1 more',
      },
      {
         items: [
            { type: ItemType.EVENT_SITE, name: 'Americas Theatre' },
            { type: ItemType.EVENT_SITE, name: 'Splash Island' },
         ],
         expected: '2 event sites: Americas Theatre and 1 more',
      },
   ];

   cases.forEach(({ items, expected }) => {
      const name = MarkerAccessibleNameFormatter.buildAccessibleName(items);

      assert.equal(name, expected);
      assert.equal(name.startsWith('2'), true);
   });
});


test('Test_BuildAccessibleName_TestMissingItemNames_ExpectTypeFallback', () => {
   const cases = [
      {
         items: [{ type: ItemType.PAVILION }, { type: ItemType.PAVILION }],
         expected: `2 pavilions: ${Strings.entityLabels.pavilion} and 1 more`,
      },
      {
         items: [{ type: ItemType.RESTROOM }, { type: ItemType.RESTROOM }],
         expected: `2 ${Strings.entityLabels.restrooms}: ${Strings.entityLabels.restroom} and 1 more`,
      },
      {
         items: [{ type: ItemType.GIFT_SHOP }, { type: ItemType.GIFT_SHOP }],
         expected: `2 ${Strings.entityLabels.giftShops}: ${Strings.entityLabels.giftShop} and 1 more`,
      },
      {
         items: [{ type: ItemType.ATTRACTION }, { type: ItemType.ATTRACTION }],
         expected: `2 ${Strings.entityLabels.attractions}: ${Strings.entityLabels.attraction} and 1 more`,
      },
      {
         items: [{ type: ItemType.TRANSPORTATION }, { type: ItemType.TRANSPORTATION }],
         expected: `2 ${Strings.entityLabels.attractions}: ${Strings.entityLabels.attraction} and 1 more`,
      },
      {
         items: [{ type: ItemType.TRANSPORTATION_STATION }, { type: ItemType.TRANSPORTATION_STATION }],
         expected: `2 stations: ${Strings.entityLabels.transportationStation} and 1 more`,
      },
      {
         items: [{ type: ItemType.GUEST_SERVICE }, { type: ItemType.GUEST_SERVICE }],
         expected: `2 guest services: ${Strings.map.hover.guestService} and 1 more`,
      },
      {
         items: [{ type: ItemType.EVENT_SITE }, { type: ItemType.EVENT_SITE }],
         expected: `2 event sites: ${Strings.map.hover.eventSite} and 1 more`,
      },
   ];

   cases.forEach(({ items, expected }) => {
      assert.equal(MarkerAccessibleNameFormatter.buildAccessibleName(items), expected);
   });
});


test('Test_BuildAccessibleName_TestGuardiansTalkWithoutName_ExpectLabelFallback', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.GUARDIANS_TALK },
      { type: ItemType.GUARDIANS_TALK },
   ]);

   assert.equal(name, `2 talks: ${Strings.entityLabels.guardiansTalk} and 1 more`);
});


test('Test_BuildAccessibleName_TestWildEncounterWithoutName_ExpectMeetingSpotFallback', () => {
   const name = MarkerAccessibleNameFormatter.buildAccessibleName([
      { type: ItemType.WILD_ENCOUNTER },
      { type: ItemType.WILD_ENCOUNTER },
   ]);

   assert.equal(
      name,
      `2 wild encounters: ${Strings.map.hover.wildEncounterMeetingSpot} and 1 more`
   );
});


test('Test_BuildAccessibleName_TestUnknownTypeCluster_ExpectHoverFallback', () => {
   const items = [
      { type: 'unknownType', name: 'Item' },
      { type: 'unknownType', name: 'Other' },
   ];
   const name = MarkerAccessibleNameFormatter.buildAccessibleName(items);

   assert.equal(name, '');
});
