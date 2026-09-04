import assert from 'node:assert/strict';
import { test } from 'node:test';

import { MarkerHoverText } from '../../../scripts/markers/markerHoverText.js';
import { APP_STRINGS } from '../../../scripts/strings.js';

test('Test_BuildHoverText_TestMissingOrHiddenTypes_ExpectEmpty', () => {
   assert.equal(MarkerHoverText.buildHoverText(null), '');
   assert.equal(MarkerHoverText.buildHoverText([]), '');
   assert.equal(
      MarkerHoverText.buildHoverText([{ type: 'transportationRouteMarker', name: 'Route' }]),
      ''
   );
   assert.equal(MarkerHoverText.buildHoverText([{ type: 'unknownType', name: 'Item' }]), '');
});

test('Test_BuildHoverText_TestCountedMapItemTypes_ExpectFormattedTitles', () => {
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
         type: 'restroom',
         items: [{ type: 'restroom', title: 'Americas Restroom' }],
         expected: 'Americas Restroom',
      },
      {
         type: 'transportation',
         items: [{ type: 'transportation', name: 'Zoomobile' }],
         expected: 'Zoomobile',
      },
      {
         type: 'drinkingFountain',
         items: [{ type: 'drinkingFountain' }, { type: 'drinkingFountain' }],
         expected: `${APP_STRINGS.map.hover.drinkingFountain} + 1`,
      },
      {
         type: 'guestService',
         items: [{ type: 'guestService', service_type: 'First Aid' }],
         expected: 'First Aid',
      },
   ];

   for (const { items, expected } of cases) {
      assert.equal(MarkerHoverText.buildHoverText(items), expected);
   }
});

test('Test_BuildHoverText_TestGuardiansTalkSingle_ExpectNamedHover', () => {
   assert.equal(
      MarkerHoverText.buildHoverText([
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
      MarkerHoverText.buildHoverText([
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
      MarkerHoverText.buildHoverText([{ type: 'guardiansTalk' }]),
      APP_STRINGS.entityLabels.guardiansTalk
   );
});

test('Test_BuildHoverText_TestWildEncounterVariants_ExpectMeetingSpotText', () => {
   assert.equal(
      MarkerHoverText.buildHoverText([
         {
            type: 'wildEncounter',
            name: 'African Rainforest',
         },
      ]),
      'Wild Encounter • African Rainforest - Meeting Spot'
   );
   assert.equal(
      MarkerHoverText.buildHoverText([{ type: 'wildEncounter' }]),
      APP_STRINGS.map.hover.wildEncounterMeetingSpot
   );
   assert.equal(
      MarkerHoverText.buildHoverText([
         { type: 'wildEncounter', name: 'African Rainforest' },
         { type: 'wildEncounter', name: 'Indo-Malaya' },
      ]),
      'Wild Encounter • African Rainforest + 1 more - Meeting Spot'
   );
});
