import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreFilter } from '../../../scripts/search/exploreFilter.js';
import { ExploreFilterBinder } from '../../../scripts/search/exploreFilterBinder.js';
import { Strings } from '../../../scripts/strings.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();

function _createCheckbox(value, { checked = false, label = value } = {}) {
   const checkbox = document.createElement('input');
   checkbox.type = 'checkbox';
   checkbox.value = value;
   checkbox.checked = checked;

   const labelEl = document.createElement('label');
   const labelText = document.createElement('span');
   labelText.textContent = label;
   labelEl.append(labelText, checkbox);
   checkbox.closest = (selector) => (selector === 'label' ? labelEl : null);

   return checkbox;
}

function _patchToggle(multiSelect) {
   multiSelect.classList.toggle = (className, shouldAdd) => {
      if (shouldAdd === undefined) {
         if (multiSelect.classList.contains(className)) {
            multiSelect.classList.remove(className);
         }
         else {
            multiSelect.classList.add(className);
         }
         return;
      }

      if (shouldAdd) {
         multiSelect.classList.add(className);
      }
      else {
         multiSelect.classList.remove(className);
      }
   };
}

test('Test_GetSelectedTransportationRoute_TestChecked_ExpectValueOrNone', () => {
   assert.equal(ExploreFilterBinder.getSelectedTransportationRoute(), 'none');

   const input = document.createElement('input');
   input.name = 'transportationRoute-zoomobile';
   input.value = 'summer';
   input.checked = true;
   document.body.appendChild(input);

   const originalQuery = document.querySelector;
   document.querySelector = (selector) => (
      selector === ExploreFilterBinder.TRANSPORTATION_ROUTE_SELECTOR ? input : originalQuery(selector)
   );

   try {
      assert.equal(ExploreFilterBinder.getSelectedTransportationRoute(), 'summer');
   } finally {
      document.querySelector = originalQuery;
   }
});

test('Test_HasTransportationRoute_TestValues_ExpectBoolean', () => {
   assert.equal(ExploreFilterBinder.hasTransportationRoute('none'), false);
   assert.equal(ExploreFilterBinder.hasTransportationRoute('summer'), true);
});

test('Test_CreateFallbackExploreFilter_TestDefault_ExpectAnimalFlags', () => {
   const original = ExploreFilter.buildExploreSearchIncludeFlags;
   ExploreFilter.buildExploreSearchIncludeFlags = (types, route) => ({ types, route });

   try {
      const filter = ExploreFilterBinder.createFallbackExploreFilter();
      assert.deepEqual(filter.getSelectedTypes(), ['animal']);
      assert.deepEqual(filter.buildSearchIncludeFlags(), {
         types: ['animal'],
         route: 'none',
      });
   } finally {
      ExploreFilter.buildExploreSearchIncludeFlags = original;
   }
});

test('Test_GetFilterRefs_TestMultiSelect_ExpectRefs', () => {
   const multiSelect = document.createElement('div');
   const button = document.createElement('button');
   button.className = 'multi-select-button';
   const dropdown = document.createElement('div');
   dropdown.className = 'multi-select-dropdown';
   const checkbox = _createCheckbox('animal');
   dropdown.appendChild(checkbox.closest('label'));
   dropdown.querySelectorAll = (selector) => (
      selector === 'input[type="checkbox"]' ? [checkbox] : []
   );
   const chipContainer = document.createElement('div');
   chipContainer.className = 'selected-values';
   multiSelect.append(button, dropdown, chipContainer);

   const refs = ExploreFilterBinder.getFilterRefs(multiSelect);
   assert.equal(refs.button, button);
   assert.equal(refs.dropdown, dropdown);
   assert.equal(refs.chipContainer, chipContainer);
   assert.equal(refs.checkboxes.length, 1);
});

test('Test_GetCheckboxLabel_TestLabelOrValue_ExpectText', () => {
   const labeled = _createCheckbox('animal', { label: 'Animals' });
   assert.equal(ExploreFilterBinder.getCheckboxLabel(labeled), 'Animals');
});

test('Test_CreateChips_TestLabels_ExpectElements', () => {
   const noneChip = ExploreFilterBinder.createNoSelectionChip();
   assert.equal(noneChip.className, 'filter-none');
   assert.equal(noneChip.textContent, Strings.map.transportationRoute.none);

   const chip = ExploreFilterBinder.createFilterChip('Animals');
   assert.equal(chip.className, 'filter-chip');
   assert.equal(chip.textContent, 'Animals');
});

test('Test_GetSelectedTypeValues_TestRoute_ExpectIncludesTransportation', () => {
   const animal = _createCheckbox('animal', { checked: true });
   const restaurant = _createCheckbox('restaurant', { checked: false });

   assert.deepEqual(
      ExploreFilterBinder.getSelectedTypeValues([animal, restaurant], 'none'),
      ['animal']
   );
   assert.deepEqual(
      ExploreFilterBinder.getSelectedTypeValues([animal, restaurant], 'summer'),
      ['animal', 'transportationRoute']
   );
});

test('Test_RenderSelectedChips_TestEmptyAndSelected_ExpectChips', () => {
   const chipContainer = document.createElement('div');
   const animal = _createCheckbox('animal', { checked: false, label: 'Animals' });

   ExploreFilterBinder.renderSelectedChips(chipContainer, [animal]);
   assert.equal(chipContainer.children[0].className, 'filter-none');

   animal.checked = true;
   ExploreFilterBinder.renderSelectedChips(chipContainer, [animal]);
   assert.equal(chipContainer.children[0].className, 'filter-chip');
   assert.equal(chipContainer.children[0].textContent, 'Animals');

   ExploreFilterBinder.renderSelectedChips(null, [animal]);
});

test('Test_CreateExploreFilterState_TestSelection_ExpectFlags', () => {
   const original = ExploreFilter.buildExploreSearchIncludeFlags;
   ExploreFilter.buildExploreSearchIncludeFlags = (types, route) => ({ types, route });

   try {
      const animal = _createCheckbox('animal', { checked: true });
      const state = ExploreFilterBinder.createExploreFilterState({
         checkboxes: [animal],
         getTransportationRoute: () => 'summer',
      });

      assert.deepEqual(state.getSelectedTypes(), ['animal', 'transportationRoute']);
      assert.deepEqual(state.buildSearchIncludeFlags(), {
         types: ['animal', 'transportationRoute'],
         route: 'summer',
      });
   } finally {
      ExploreFilter.buildExploreSearchIncludeFlags = original;
   }
});

test('Test_BindDropdownAndCheckboxEvents_TestInteractions_ExpectCallbacks', () => {
   const multiSelect = document.createElement('div');
   _patchToggle(multiSelect);
   const button = document.createElement('button');
   const dropdown = document.createElement('div');
   const checkbox = _createCheckbox('animal', { checked: true });
   const documentListeners = {};
   const originalAdd = document.addEventListener;

   document.addEventListener = (eventName, handler) => {
      documentListeners[eventName] = handler;
   };

   const changes = [];
   const unchecked = [];
   const selectionChanged = [];

   ExploreFilterBinder.bindDropdownEvents({ multiSelect, button, dropdown });
   button.listeners.click({ stopPropagation() {} });
   assert.equal(multiSelect.classList.contains('open'), true);
   dropdown.listeners.click({ stopPropagation() {} });
   documentListeners.click();
   assert.equal(multiSelect.classList.contains('open'), false);

   ExploreFilterBinder.bindCheckboxEvents({
      checkboxes: [checkbox],
      getSelectedTypes: () => [],
      onAnimalsUnchecked: () => unchecked.push(true),
      onChange: () => changes.push(true),
      onSelectionChanged: () => selectionChanged.push(true),
   });

   checkbox.listeners.change();
   assert.deepEqual(selectionChanged, [true]);
   assert.deepEqual(unchecked, [true]);
   assert.deepEqual(changes, [true]);

   document.addEventListener = originalAdd;
});
