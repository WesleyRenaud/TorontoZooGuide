import assert from 'node:assert/strict';
import { test } from 'node:test';

import { MarkerHoverFormatter } from '../../../scripts/markers/markerHoverFormatter.js';
import { Strings } from '../../../scripts/strings.js';

test('Test_BuildHoverText_TestMissingOrHiddenTypes_ExpectEmpty', () => {
   assert.equal(MarkerHoverFormatter.buildHoverText(null), '');
   assert.equal(MarkerHoverFormatter.buildHoverText([]), '');
   assert.equal(
      MarkerHoverFormatter.buildHoverText([{ type: 'transportationRouteMarker', name: 'Route' }]),
      ''
   );
   assert.equal(MarkerHoverFormatter.buildHoverText([{ type: 'unknownType', name: 'Item' }]), '');
});

test('Test_BuildHoverText_TestCountedItemTypes_ExpectFormattedTitles', () => {
   const cases = [
      {
         type: 'animal',
         items: [{ type: 'animal', species: 'African Lion' }],
         expected: 'African Lion',
      },
      {
         type: 'animal',
         items: [
            { type: 'animal', species: 'African Lion' },
            { type: 'animal', species: 'Amur Tiger' },
         ],
         expected: 'African Lion + 1',
      },
      {
         type: 'pavilion',
         items: [{ type: 'pavilion', name: 'Americas Pavilion' }],
         expected: 'Americas Pavilion',
      },
      {
         type: 'restaurant',
         items: [{ type: 'restaurant', name: 'Peaks Cafe' }],
         expected: 'Peaks Cafe',
      },
      {
         type: 'restroom',
         items: [{ type: 'restroom', title: 'Americas Restroom' }],
         expected: 'Americas Restroom',
      },
      {
         type: 'giftShop',
         items: [{ type: 'giftShop', name: 'Zootique' }],
         expected: 'Zootique',
      },
      {
         type: 'attraction',
         items: [{ type: 'attraction', name: 'Carousel' }],
         expected: 'Carousel',
      },
      {
         type: 'transportation',
         items: [{ type: 'transportation', name: 'Zoomobile' }],
         expected: 'Zoomobile',
      },
      {
         type: 'transportationStation',
         items: [{ type: 'transportationStation', name: 'Station 1' }],
         expected: 'Station 1',
      },
      {
         type: 'drinkingFountain',
         items: [{ type: 'drinkingFountain' }, { type: 'drinkingFountain' }],
         expected: `${Strings.map.hover.drinkingFountain} + 1`,
      },
      {
         type: 'defibrillator',
         items: [{ type: 'defibrillator' }],
         expected: Strings.map.hover.defibrillator,
      },
      {
         type: 'emergencyIntercom',
         items: [{ type: 'emergencyIntercom' }],
         expected: Strings.map.hover.emergencyIntercom,
      },
      {
         type: 'guestService',
         items: [{ type: 'guestService', service_type: 'First Aid' }],
         expected: 'First Aid',
      },
      {
         type: 'picnicSite',
         items: [{ type: 'picnicSite' }],
         expected: Strings.map.hover.picnicSite,
      },
      {
         type: 'eventSite',
         items: [{ type: 'eventSite', name: 'Tundra Trek' }],
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
            type: 'guardiansTalk',
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
            type: 'guardiansTalk',
            name: 'Amur Tiger',
         },
         {
            type: 'guardiansTalk',
            name: 'African Lion',
         },
      ]),
      'Amur Tiger Meet The Guardians Talk + 1'
   );
   assert.equal(
      MarkerHoverFormatter.buildHoverText([{ type: 'guardiansTalk' }]),
      Strings.entityLabels.guardiansTalk
   );
});

test('Test_BuildHoverText_TestWildEncounterVariants_ExpectMeetingSpotText', () => {
   assert.equal(
      MarkerHoverFormatter.buildHoverText([
         {
            type: 'wildEncounter',
            name: 'African Rainforest',
         },
      ]),
      'Wild Encounter • African Rainforest - Meeting Spot'
   );
   assert.equal(
      MarkerHoverFormatter.buildHoverText([{ type: 'wildEncounter' }]),
      Strings.map.hover.wildEncounterMeetingSpot
   );
   assert.equal(
      MarkerHoverFormatter.buildHoverText([
         { type: 'wildEncounter', name: 'African Rainforest' },
         { type: 'wildEncounter', name: 'Indo-Malaya' },
      ]),
      'Wild Encounter • African Rainforest + 1 more - Meeting Spot'
   );
});
