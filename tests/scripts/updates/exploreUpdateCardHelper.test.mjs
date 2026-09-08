import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreUpdateCardHelper } from '../../../scripts/updates/exploreUpdateCardHelper.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateUpdateTypeEl_TestTypedUpdate_ExpectClassAndLabel', () => {
   const typeEl = ExploreUpdateCardHelper.createUpdateTypeEl({ type: 'Animal Closure' });

   assert.equal(typeEl.tagName.toUpperCase(), 'SPAN');
   assert.equal(typeEl.className, 'explore-update-type explore-update-type-animal-closure');
   assert.equal(typeEl.textContent, 'Animal Closure');
});

test('Test_CreateUpdateTypeEl_TestMissingType_ExpectFallbackLabel', () => {
   const typeEl = ExploreUpdateCardHelper.createUpdateTypeEl({});

   assert.equal(typeEl.textContent, Strings.labels.update);
   assert.equal(typeEl.className, 'explore-update-type explore-update-type-');
});
