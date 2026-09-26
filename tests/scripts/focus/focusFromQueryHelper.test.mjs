import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusFromQueryHelper } from '../../../scripts/focus/focusFromQueryHelper.js';


test('Test_GetFocusRequestFromQuery_TestSpeciesAndExhibit_ExpectRequest', () => {
   const species = 'African Lion';
   const exhibit = 'African Savanna';
   const search = `?focus=${encodeURIComponent(species)}&exhibit=${encodeURIComponent(exhibit)}`;

   const request = FocusFromQueryHelper.getFocusRequestFromQuery(search);

   assert.deepEqual(request, { species, exhibit });
});


test('Test_GetFocusRequestFromQuery_TestSpeciesOnly_ExpectNullExhibit', () => {
   const species = 'African Lion';
   const search = `?focus=${encodeURIComponent(species)}`;

   const request = FocusFromQueryHelper.getFocusRequestFromQuery(search);

   assert.deepEqual(request, { species, exhibit: null });
});


test('Test_GetFocusRequestFromQuery_TestMissingFocus_ExpectNull', () => {
   const search = '?other=1';

   const request = FocusFromQueryHelper.getFocusRequestFromQuery(search);

   assert.equal(request, null);
});
