import assert from 'node:assert/strict';
import { test } from 'node:test';

import { MarkerHoverFormatter } from '../../../scripts/markers/markerHoverFormatter.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Strings } from '../../../scripts/strings.js';

test('Test_BuildHoverText_TestMissingOrHiddenTypes_ExpectEmpty', () => {
   assert.equal(MarkerHoverFormatter.buildHoverText(null), '');
   assert.equal(MarkerHoverFormatter.buildHoverText([]), '');
   assert.equal(
      MarkerHoverFormatter.buildHoverText([{ type: ItemType.TRANSPORTATION_ROUTE_MARKER, name: 'Route' }]),
      ''
   );
   assert.equal(MarkerHoverFormatter.buildHoverText([{ type: 'unknownType', name: 'Item' }]), '');
});

test('Test_BuildHoverText_TestCountedItemTypes_ExpectFormattedTitles', () => {
   const cases = [
      {
         type: ItemType.ANIMAL,
         items: [{ type: ItemType.ANIMAL, species: 'African Lion' }],
         expected: 'African Lion',
      },
      {
         type: ItemType.ANIMAL,
         items: [
            { type: ItemType.ANIMAL, species: 'African Lion' },
            { type: ItemType.ANIMAL, species: 'Amur Tiger' },
         ],
         expected: 'African Lion + 1',
      },
      {
         type: ItemType.PAVILION,
         items: [{ type: ItemType.PAVILION, name: 'Americas Pavilion' }],
         expected: 'Americas Pavilion',
      },
      {
         type: ItemType.RESTAURANT,
         items: [{ type: ItemType.RESTAURANT, name: 'Peaks Cafe' }],
         expected: 'Peaks Cafe',
      },
      {
         type: ItemType.RESTROOM,
         items: [{ type: ItemType.RESTROOM, title: 'Americas Restroom' }],
         expected: 'Americas Restroom',
      },
      {
         type: ItemType.GIFT_SHOP,
         items: [{ type: ItemType.GIFT_SHOP, name: 'Zootique' }],
         expected: 'Zootique',
      },
      {
         type: ItemType.ATTRACTION,
         items: [{ type: ItemType.ATTRACTION, name: 'Carousel' }],
         expected: 'Carousel',
      },
      {
         type: ItemType.TRANSPORTATION,
         items: [{ type: ItemType.TRANSPORTATION, name: 'Zoomobile' }],
         expected: 'Zoomobile',
      },
      {
         type: ItemType.TRANSPORTATION_STATION,
         items: [{ type: ItemType.TRANSPORTATION_STATION, name: 'Station 1' }],
         expected: 'Station 1',
      },
      {
         type: ItemType.DRINKING_FOUNTAIN,
         items: [{ type: ItemType.DRINKING_FOUNTAIN }, { type: ItemType.DRINKING_FOUNTAIN }],
         expected: `${Strings.map.hover.drinkingFountain} + 1`,
      },
      {
         type: ItemType.DEFIBRILLATOR,
         items: [{ type: ItemType.DEFIBRILLATOR }],
         expected: Strings.map.hover.defibrillator,
      },
      {
         type: ItemType.EMERGENCY_INTERCOM,
         items: [{ type: ItemType.EMERGENCY_INTERCOM }],
         expected: Strings.map.hover.emergencyIntercom,
      },
      {
         type: ItemType.GUEST_SERVICE,
         items: [{ type: ItemType.GUEST_SERVICE, service_type: 'First Aid' }],
         expected: 'First Aid',
      },
      {
         type: ItemType.PICNIC_SITE,
         items: [{ type: ItemType.PICNIC_SITE }],
         expected: Strings.map.hover.picnicSite,
      },
      {
         type: ItemType.EVENT_SITE,
         items: [{ type: ItemType.EVENT_SITE, name: 'Tundra Trek' }],
         expected: 'Tundra Trek',
      },
   ];

   for (const { items, expected } of cases) {
      assert.equal(MarkerHoverFormatter.buildHoverText(items), expected);
   }
});
test('Test_BuildHoverText_TestGuardiansTalkSingle_ExpectNamedHover', () => {
   assert.equal(
      MarkerHoverFormatter.buildHoverText([
         {
            type: ItemType.GUARDIANS_TALK,
            name: 'Amur Tiger',
         },
      ]),
      'Amur Tiger Meet The Guardians Talk'
   );
});

test('Test_BuildHoverText_TestGuardiansTalkCounted_ExpectPlusCount', () => {
   assert.equal(
      MarkerHoverFormatter.buildHoverText([
         {
            type: ItemType.GUARDIANS_TALK,
            name: 'Amur Tiger',
         },
         {
            type: ItemType.GUARDIANS_TALK,
            name: 'African Lion',
         },
      ]),
      'Amur Tiger Meet The Guardians Talk + 1'
   );
   assert.equal(
      MarkerHoverFormatter.buildHoverText([{ type: ItemType.GUARDIANS_TALK }]),
      Strings.entityLabels.guardiansTalk
   );
});

test('Test_BuildHoverText_TestWildEncounterVariants_ExpectMeetingSpotText', () => {
   assert.equal(
      MarkerHoverFormatter.buildHoverText([
         {
            type: ItemType.WILD_ENCOUNTER,
            name: 'African Rainforest',
         },
      ]),
      'Wild Encounter • African Rainforest - Meeting Spot'
   );
   assert.equal(
      MarkerHoverFormatter.buildHoverText([{ type: ItemType.WILD_ENCOUNTER }]),
      Strings.map.hover.wildEncounterMeetingSpot
   );
   assert.equal(
      MarkerHoverFormatter.buildHoverText([
         { type: ItemType.WILD_ENCOUNTER, name: 'African Rainforest' },
         { type: ItemType.WILD_ENCOUNTER, name: 'Indo-Malaya' },
      ]),
      'Wild Encounter • African Rainforest + 1 more - Meeting Spot'
   );
});
