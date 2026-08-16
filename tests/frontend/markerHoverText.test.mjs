import assert from 'node:assert/strict';
import { test } from 'node:test';

import { buildHoverText } from '../../scripts/markers/markerHoverText.js';
import { APP_STRINGS } from '../../scripts/strings.js';

test('buildHoverText returns empty text for missing or hidden marker types', () => {
   assert.equal(buildHoverText(null), '');
   assert.equal(buildHoverText([]), '');
   assert.equal(buildHoverText([{ type: 'zoomobileRouteMarker', name: 'Route' }]), '');
   assert.equal(buildHoverText([{ type: 'unknownType', name: 'Item' }]), '');
});

test('buildHoverText formats counted hover text for map item types', () => {
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
      assert.equal(buildHoverText(items), expected);
   }
});

test('formats Meet the Guardians talk marker hover text', () => {
   assert.equal(
      buildHoverText([
         {
            type: 'guardiansTalk',
            name: 'Amur Tiger',
         },
      ]),
      'Amur Tiger Meet The Guardians Talk'
   );
});

test('formats counted Meet the Guardians talk marker hover text', () => {
   assert.equal(
      buildHoverText([
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
      buildHoverText([{ type: 'guardiansTalk' }]),
      APP_STRINGS.entityLabels.guardiansTalk
   );
});

test('formats wild encounter marker hover text', () => {
   assert.equal(
      buildHoverText([
         {
            type: 'wildEncounter',
            name: 'African Rainforest',
         },
      ]),
      'Wild Encounter • African Rainforest - Meeting Spot'
   );
   assert.equal(
      buildHoverText([{ type: 'wildEncounter' }]),
      APP_STRINGS.map.hover.wildEncounterMeetingSpot
   );
   assert.equal(
      buildHoverText([
         { type: 'wildEncounter', name: 'African Rainforest' },
         { type: 'wildEncounter', name: 'Indo-Malaya' },
      ]),
      'Wild Encounter • African Rainforest + 1 more - Meeting Spot'
   );
});
