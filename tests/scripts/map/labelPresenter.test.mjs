import assert from 'node:assert/strict';
import test from 'node:test';

import { LabelPresenter } from '../../../scripts/map/labelPresenter.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_InitLabelVisibilityToggle_TestChecked_ExpectLabelsVisible', () => {
   const checkboxEl = document.createElement('input');
   checkboxEl.type = 'checkbox';
   checkboxEl.checked = true;
   const rootEl = document.createElement('div');

   LabelPresenter.initLabelVisibilityToggle({ checkboxEl, rootEl });

   assert.equal(rootEl.classList.contains('hide-map-labels'), false);
});


test('Test_InitLabelVisibilityToggle_TestUnchecked_ExpectLabelsHidden', () => {
   const checkboxEl = document.createElement('input');
   checkboxEl.type = 'checkbox';
   checkboxEl.checked = true;
   const rootEl = document.createElement('div');
   LabelPresenter.initLabelVisibilityToggle({ checkboxEl, rootEl });
   checkboxEl.checked = false;

   checkboxEl.listeners.change?.();

   assert.equal(rootEl.classList.contains('hide-map-labels'), true);
});


test('Test_InitLabelVisibilityToggle_TestMissingElements_ExpectNoThrow', () => {
   const options = {};

   const initialize = () => LabelPresenter.initLabelVisibilityToggle(options);

   assert.doesNotThrow(initialize);
});
