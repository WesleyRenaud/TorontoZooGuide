import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalViewingScopeControlHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeControlHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createFieldGrid() {
   const fieldEl = document.createElement('div');
   fieldEl.className = 'console-operations-field';
   const gridEl = document.createElement('div');
   fieldEl.appendChild(gridEl);
   return { fieldEl, gridEl };
}

test('Test_PopulateAndSelectedEnclosureNames_TestCheckedOptions_ExpectNames', () => {
   const { fieldEl, gridEl } = _createFieldGrid();

   AnimalViewingScopeControlHelper.populateOptions(gridEl, [
      { enclosureName: 'Male Herd', label: 'Male Herd' },
      { enclosureName: '', label: 'Main' },
   ]);

   assert.equal(fieldEl.classList.contains('is-invisible'), false);
   assert.deepEqual(
      AnimalViewingScopeControlHelper.selectedEnclosureNames(gridEl),
      [ 'Male Herd', '' ]
   );

   gridEl.querySelectorAll('input[type="checkbox"]')[0].checked = false;
   assert.deepEqual(
      AnimalViewingScopeControlHelper.selectedEnclosureNames(gridEl),
      [ '' ]
   );

   AnimalViewingScopeControlHelper.clearOptions(gridEl);
   assert.equal(gridEl.children.length, 0);
   assert.equal(fieldEl.classList.contains('is-invisible'), true);
});

test('Test_PopulateOptions_TestSingleEnclosure_ExpectFieldHidden', () => {
   const { fieldEl, gridEl } = _createFieldGrid();

   AnimalViewingScopeControlHelper.populateOptions(gridEl, [
      { enclosureName: '', label: 'Main' },
   ]);

   assert.equal(fieldEl.classList.contains('is-invisible'), true);
   assert.deepEqual(
      AnimalViewingScopeControlHelper.selectedEnclosureNames(gridEl),
      [ '' ]
   );
});

test('Test_PopulateOptions_TestSingleClosedAmongMany_ExpectFieldVisible', () => {
   const { fieldEl, gridEl } = _createFieldGrid();

   AnimalViewingScopeControlHelper.populateOptions(gridEl, [
      { enclosureName: 'Indoor', label: 'Indoor' },
   ], {
      isFieldVisible: true,
   });

   assert.equal(fieldEl.classList.contains('is-invisible'), false);
   assert.deepEqual(
      AnimalViewingScopeControlHelper.selectedEnclosureNames(gridEl),
      [ 'Indoor' ]
   );
});
