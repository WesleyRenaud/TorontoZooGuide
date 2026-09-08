import assert from 'node:assert/strict';
import test from 'node:test';
import { mock } from 'node:test';

import { FocusRequest } from '../../../scripts/map/focusRequest.js';

test('Test_NormalizeSearchFocusRequest_TestPayload_ExpectNormalizedOrNull', () => {
   assert.equal(FocusRequest.normalizeSearchFocusRequest(null), null);
   assert.equal(FocusRequest.normalizeSearchFocusRequest({ species: 'Lion' }), null);
   assert.deepEqual(FocusRequest.normalizeSearchFocusRequest({
      type: 'animal',
      species: 'Lion',
   }), {
      type: 'animal',
      row: {
         type: 'animal',
         species: 'Lion',
      },
   });
});

test('Test_ResolveDeepLinkFocus_TestModes_ExpectDirectOrRefetch', () => {
   assert.equal(FocusRequest.resolveDeepLinkFocus(null), null);
   assert.deepEqual(FocusRequest.resolveDeepLinkFocus({
      row: { type: 'attraction', name: 'Carousel' },
   }), {
      mode: 'direct',
      focusRequest: {
         row: { type: 'attraction', name: 'Carousel' },
         type: 'attraction',
      },
   });
   assert.deepEqual(FocusRequest.resolveDeepLinkFocus({
      species: 'African Lion',
      exhibit: 'Savanna',
   }), {
      mode: 'refetch',
      focusRequest: {
         type: 'animal',
         row: {
            type: 'animal',
            species: 'African Lion',
            exhibit: 'Savanna',
         },
      },
   });
   assert.equal(FocusRequest.resolveDeepLinkFocus({ row: { name: 'x' } }), null);
   assert.equal(FocusRequest.resolveDeepLinkFocus({ exhibit: 'Savanna' }), null);
   assert.equal(FocusRequest.resolveDeepLinkFocus({}), null);
});

test('Test_ScheduleFocusRequest_TestRow_ExpectDeferredFocus', () => {
   mock.timers.enable({ apis: ['setTimeout'] });
   const focuses = [];

   try {
      FocusRequest.scheduleFocusRequest({
         focus: (args) => { focuses.push(args); },
      }, {
         type: 'animal',
         row: { species: 'Lion' },
      });
      assert.deepEqual(focuses, []);
      mock.timers.tick(0);
      assert.deepEqual(focuses, [{
         row: { species: 'Lion' },
         type: 'animal',
      }]);

      FocusRequest.scheduleFocusRequest({ focus: () => {} }, {});
   } finally {
      mock.timers.reset();
   }
});
