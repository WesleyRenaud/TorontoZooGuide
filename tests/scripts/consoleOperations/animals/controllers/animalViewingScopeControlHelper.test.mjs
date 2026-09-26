import assert from 'node:assert/strict';
import test from 'node:test';

import { AnimalViewingScopeControlHelper } from '../../../../../scripts/consoleOperations/animals/controllers/animalViewingScopeControlHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createFieldGrid() {
   const fieldEl = document.createElement('div');
   fieldEl.className = 'console-operations-field';
   const gridEl = document.createElement('div');
   fieldEl.appendChild(gridEl);
   return { fieldEl, gridEl };
}


test('Test_PopulateOptions_TestCheckedOptions_ExpectSelectedNames', () => {
   const maleHerd = 'Male Herd';
   const unnamed = '';
   const { fieldEl, gridEl } = _createFieldGrid();

   AnimalViewingScopeControlHelper.populateOptions(gridEl, [
      { enclosureName: maleHerd, label: maleHerd },
      { enclosureName: unnamed, label: 'Main' },
   ]);

   const selected = AnimalViewingScopeControlHelper.selectedEnclosureNames(gridEl);

   assert.equal(fieldEl.classList.contains('is-invisible'), false);
   assert.deepEqual(selected, [maleHerd, unnamed]);
});


test('Test_SelectedEnclosureNames_TestUncheckedOption_ExpectRemainingName', () => {
   const maleHerd = 'Male Herd';
   const unnamed = '';
   const { gridEl } = _createFieldGrid();
   AnimalViewingScopeControlHelper.populateOptions(gridEl, [
      { enclosureName: maleHerd, label: maleHerd },
      { enclosureName: unnamed, label: 'Main' },
   ]);

   gridEl.querySelectorAll('input[type="checkbox"]')[Position.FIRST].checked = false;
   const selected = AnimalViewingScopeControlHelper.selectedEnclosureNames(gridEl);

   assert.deepEqual(selected, [unnamed]);
});


test('Test_ClearOptions_TestPopulatedGrid_ExpectEmptyAndHidden', () => {
   const { fieldEl, gridEl } = _createFieldGrid();
   AnimalViewingScopeControlHelper.populateOptions(gridEl, [
      { enclosureName: 'Male Herd', label: 'Male Herd' },
      { enclosureName: '', label: 'Main' },
   ]);

   AnimalViewingScopeControlHelper.clearOptions(gridEl);

   assert.equal(gridEl.children.length, 0);
   assert.equal(fieldEl.classList.contains('is-invisible'), true);
});


test('Test_PopulateOptions_TestSingleEnclosure_ExpectFieldHidden', () => {
   const unnamed = '';
   const { fieldEl, gridEl } = _createFieldGrid();

   AnimalViewingScopeControlHelper.populateOptions(gridEl, [
      { enclosureName: unnamed, label: 'Main' },
   ]);

   const selected = AnimalViewingScopeControlHelper.selectedEnclosureNames(gridEl);

   assert.equal(fieldEl.classList.contains('is-invisible'), true);
   assert.deepEqual(selected, [unnamed]);
});


test('Test_PopulateOptions_TestSingleClosedAmongMany_ExpectFieldVisible', () => {
   const indoor = 'Indoor';
   const { fieldEl, gridEl } = _createFieldGrid();

   AnimalViewingScopeControlHelper.populateOptions(gridEl, [
      { enclosureName: indoor, label: indoor },
   ], {
      isFieldVisible: true,
   });

   const selected = AnimalViewingScopeControlHelper.selectedEnclosureNames(gridEl);

   assert.equal(fieldEl.classList.contains('is-invisible'), false);
   assert.deepEqual(selected, [indoor]);
});
