import assert from 'node:assert/strict';
import test from 'node:test';
import { mock } from 'node:test';

import { FocusRequest } from '../../../scripts/map/focusRequest.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';


test('Test_NormalizeSearchFocusRequest_TestNull_ExpectNull', () => {
   const request = null;

   const normalized = FocusRequest.normalizeSearchFocusRequest(request);

   assert.equal(normalized, null);
});


test('Test_NormalizeSearchFocusRequest_TestMissingType_ExpectNull', () => {
   const request = { species: 'Lion' };

   const normalized = FocusRequest.normalizeSearchFocusRequest(request);

   assert.equal(normalized, null);
});


test('Test_NormalizeSearchFocusRequest_TestAnimal_ExpectNormalized', () => {
   const type = ItemType.ANIMAL;
   const species = 'Lion';
   const request = { type, species };

   const normalized = FocusRequest.normalizeSearchFocusRequest(request);

   assert.deepEqual(normalized, {
      type,
      row: {
         type,
         species,
      },
   });
});


test('Test_ResolveDeepLinkFocus_TestNull_ExpectNull', () => {
   const request = null;

   const resolved = FocusRequest.resolveDeepLinkFocus(request);

   assert.equal(resolved, null);
});


test('Test_ResolveDeepLinkFocus_TestAttractionRow_ExpectDirect', () => {
   const type = ItemType.ATTRACTION;
   const name = 'Carousel';
   const request = { row: { type, name } };

   const resolved = FocusRequest.resolveDeepLinkFocus(request);

   assert.deepEqual(resolved, {
      mode: 'direct',
      focusRequest: {
         row: { type, name },
         type,
      },
   });
});


test('Test_ResolveDeepLinkFocus_TestSpeciesAndExhibit_ExpectRefetch', () => {
   const species = 'African Lion';
   const exhibit = 'Savanna';
   const request = { species, exhibit };

   const resolved = FocusRequest.resolveDeepLinkFocus(request);

   assert.deepEqual(resolved, {
      mode: 'refetch',
      focusRequest: {
         type: ItemType.ANIMAL,
         row: {
            type: ItemType.ANIMAL,
            species,
            exhibit,
         },
      },
   });
});


test('Test_ResolveDeepLinkFocus_TestUntypedRow_ExpectNull', () => {
   const request = { row: { name: 'x' } };

   const resolved = FocusRequest.resolveDeepLinkFocus(request);

   assert.equal(resolved, null);
});


test('Test_ResolveDeepLinkFocus_TestExhibitOnly_ExpectNull', () => {
   const request = { exhibit: 'Savanna' };

   const resolved = FocusRequest.resolveDeepLinkFocus(request);

   assert.equal(resolved, null);
});


test('Test_ResolveDeepLinkFocus_TestEmpty_ExpectNull', () => {
   const request = {};

   const resolved = FocusRequest.resolveDeepLinkFocus(request);

   assert.equal(resolved, null);
});


test('Test_ScheduleFocusRequest_TestRow_ExpectDeferredFocus', () => {
   mock.timers.enable({ apis: ['setTimeout'] });
   const focuses = [];
   const type = ItemType.ANIMAL;
   const row = { species: 'Lion' };

   try {
      FocusRequest.scheduleFocusRequest({
         focus: (args) => { focuses.push(args); },
      }, {
         type,
         row,
      });
      mock.timers.tick(0);

      assert.deepEqual(focuses, [{ row, type }]);
   } finally {
      mock.timers.reset();
   }
});


test('Test_ScheduleFocusRequest_TestEmpty_ExpectNoThrow', () => {
   mock.timers.enable({ apis: ['setTimeout'] });

   try {
      const schedule = () => FocusRequest.scheduleFocusRequest({ focus: () => {} }, {});

      assert.doesNotThrow(schedule);
   } finally {
      mock.timers.reset();
   }
});
