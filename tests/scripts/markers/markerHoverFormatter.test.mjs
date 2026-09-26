import assert from 'node:assert/strict';
import { test } from 'node:test';

import { MarkerHoverFormatter } from '../../../scripts/markers/markerHoverFormatter.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Strings } from '../../../scripts/strings.js';

const africanLion = 'African Lion';
const amurTiger = 'Amur Tiger';
const africanRainforest = 'African Rainforest';


test('Test_BuildHoverText_TestMissing_ExpectEmpty', () => {
   const hover = MarkerHoverFormatter.buildHoverText(null);

   assert.equal(hover, '');
});


test('Test_BuildHoverText_TestEmpty_ExpectEmpty', () => {
   const hover = MarkerHoverFormatter.buildHoverText([]);

   assert.equal(hover, '');
});


test('Test_BuildHoverText_TestRouteMarker_ExpectEmpty', () => {
   const hover = MarkerHoverFormatter.buildHoverText([
      { type: ItemType.TRANSPORTATION_ROUTE_MARKER, name: 'Route' },
   ]);

   assert.equal(hover, '');
});


test('Test_BuildHoverText_TestUnknownType_ExpectEmpty', () => {
   const hover = MarkerHoverFormatter.buildHoverText([{ type: 'unknownType', name: 'Item' }]);

   assert.equal(hover, '');
});


test('Test_BuildHoverText_TestCountedItemTypes_ExpectFormattedTitles', () => {
   const cases = [
      {
         items: [{ type: ItemType.ANIMAL, species: africanLion }],
         expected: africanLion,
      },
      {
         items: [
            { type: ItemType.ANIMAL, species: africanLion },
            { type: ItemType.ANIMAL, species: amurTiger },
         ],
         expected: `${africanLion} ${Strings.format.moreCount(1)}`,
      },
      {
         items: [{ type: ItemType.PAVILION, name: 'Americas Pavilion' }],
         expected: 'Americas Pavilion',
      },
      {
         items: [{ type: ItemType.RESTAURANT, name: 'Peaks Cafe' }],
         expected: 'Peaks Cafe',
      },
      {
         items: [{ type: ItemType.RESTROOM, title: 'Americas Restroom' }],
         expected: 'Americas Restroom',
      },
      {
         items: [{ type: ItemType.GIFT_SHOP, name: 'Zootique' }],
         expected: 'Zootique',
      },
      {
         items: [{ type: ItemType.ATTRACTION, name: 'Carousel' }],
         expected: 'Carousel',
      },
      {
         items: [{ type: ItemType.TRANSPORTATION, name: 'Zoomobile' }],
         expected: 'Zoomobile',
      },
      {
         items: [{ type: ItemType.TRANSPORTATION_STATION, name: 'Station 1' }],
         expected: 'Station 1',
      },
      {
         items: [{ type: ItemType.DRINKING_FOUNTAIN }, { type: ItemType.DRINKING_FOUNTAIN }],
         expected: `${Strings.map.hover.drinkingFountain} ${Strings.format.moreCount(1)}`,
      },
      {
         items: [{ type: ItemType.DEFIBRILLATOR }],
         expected: Strings.map.hover.defibrillator,
      },
      {
         items: [{ type: ItemType.EMERGENCY_INTERCOM }],
         expected: Strings.map.hover.emergencyIntercom,
      },
      {
         items: [{ type: ItemType.GUEST_SERVICE, service_type: 'First Aid' }],
         expected: 'First Aid',
      },
      {
         items: [{ type: ItemType.PICNIC_SITE }],
         expected: Strings.map.hover.picnicSite,
      },
      {
         items: [{ type: ItemType.EVENT_SITE, name: 'Tundra Trek' }],
         expected: 'Tundra Trek',
      },
   ];

   for (const { items, expected } of cases) {
      const hover = MarkerHoverFormatter.buildHoverText(items);

      assert.equal(hover, expected);
   }
});


test('Test_BuildHoverText_TestGuardiansTalkSingle_ExpectNamedHover', () => {
   const name = amurTiger;

   const hover = MarkerHoverFormatter.buildHoverText([
      {
         type: ItemType.GUARDIANS_TALK,
         name,
      },
   ]);

   assert.equal(hover, Strings.map.hover.guardiansTalkWithName(name));
});


test('Test_BuildHoverText_TestGuardiansTalkCounted_ExpectPlusCount', () => {
   const name = amurTiger;

   const hover = MarkerHoverFormatter.buildHoverText([
      {
         type: ItemType.GUARDIANS_TALK,
         name,
      },
      {
         type: ItemType.GUARDIANS_TALK,
         name: africanLion,
      },
   ]);

   assert.equal(
      hover,
      `${Strings.map.hover.guardiansTalkWithName(name)} ${Strings.format.moreCount(1)}`
   );
});


test('Test_BuildHoverText_TestGuardiansTalkUnnamed_ExpectLabel', () => {
   const hover = MarkerHoverFormatter.buildHoverText([{ type: ItemType.GUARDIANS_TALK }]);

   assert.equal(hover, Strings.entityLabels.guardiansTalk);
});


test('Test_BuildHoverText_TestWildEncounterNamed_ExpectMeetingSpot', () => {
   const hover = MarkerHoverFormatter.buildHoverText([
      {
         type: ItemType.WILD_ENCOUNTER,
         name: africanRainforest,
      },
   ]);

   assert.equal(hover, Strings.map.hover.wildEncounterMeetingSpotWithName(africanRainforest));
});


test('Test_BuildHoverText_TestWildEncounterUnnamed_ExpectMeetingSpot', () => {
   const hover = MarkerHoverFormatter.buildHoverText([{ type: ItemType.WILD_ENCOUNTER }]);

   assert.equal(hover, Strings.map.hover.wildEncounterMeetingSpot);
});


test('Test_BuildHoverText_TestWildEncounterMultiple_ExpectMore', () => {
   const hover = MarkerHoverFormatter.buildHoverText([
      { type: ItemType.WILD_ENCOUNTER, name: africanRainforest },
      { type: ItemType.WILD_ENCOUNTER, name: 'Indo-Malaya' },
   ]);

   assert.equal(hover, Strings.map.hover.wildEncounterMultiple(africanRainforest, 1));
});
