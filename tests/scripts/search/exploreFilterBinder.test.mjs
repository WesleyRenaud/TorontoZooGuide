import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreFilter } from '../../../scripts/search/exploreFilter.js';
import { ExploreFilterBinder } from '../../../scripts/search/exploreFilterBinder.js';
import { Strings } from '../../../scripts/strings.js';
import { ItemType } from '../../../scripts/shared/enums/itemType.js';
import { Position } from '../../../scripts/shared/enums/position.js';
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


test('Test_GetSelectedTransportationRoute_TestMissing_ExpectNone', () => {
   const route = ExploreFilterBinder.getSelectedTransportationRoute();

   assert.equal(route, 'none');
});


test('Test_GetSelectedTransportationRoute_TestChecked_ExpectValue', () => {
   const value = 'summer';
   const input = document.createElement('input');
   input.name = 'transportationRoute-zoomobile';
   input.value = value;
   input.checked = true;
   document.body.appendChild(input);
   const originalQuery = document.querySelector;
   document.querySelector = (selector) => (
      selector === ExploreFilterBinder.TRANSPORTATION_ROUTE_SELECTOR ? input : originalQuery(selector)
   );

   try {
      const route = ExploreFilterBinder.getSelectedTransportationRoute();

      assert.equal(route, value);
   } finally {
      document.querySelector = originalQuery;
   }
});


test('Test_HasTransportationRoute_TestNone_ExpectFalse', () => {
   const hasRoute = ExploreFilterBinder.hasTransportationRoute('none');

   assert.equal(hasRoute, false);
});


test('Test_HasTransportationRoute_TestSummer_ExpectTrue', () => {
   const hasRoute = ExploreFilterBinder.hasTransportationRoute('summer');

   assert.equal(hasRoute, true);
});


test('Test_CreateFallbackExploreFilter_TestDefault_ExpectAnimalFlags', () => {
   const original = ExploreFilter.buildExploreSearchIncludeFlags;
   ExploreFilter.buildExploreSearchIncludeFlags = (types, route) => ({ types, route });

   try {
      const filter = ExploreFilterBinder.createFallbackExploreFilter();

      assert.deepEqual(filter.getSelectedTypes(), [ItemType.ANIMAL]);
      assert.deepEqual(filter.buildSearchIncludeFlags(), {
         types: [ItemType.ANIMAL],
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
   const checkbox = _createCheckbox(ItemType.ANIMAL);
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
   assert.equal(refs.checkboxes.length, Position.SECOND);
});


test('Test_GetCheckboxLabel_TestLabel_ExpectText', () => {
   const label = 'Animals';
   const labeled = _createCheckbox(ItemType.ANIMAL, { label });

   const text = ExploreFilterBinder.getCheckboxLabel(labeled);

   assert.equal(text, label);
});


test('Test_CreateNoSelectionChip_TestDefault_ExpectNone', () => {
   const noneChip = ExploreFilterBinder.createNoSelectionChip();

   assert.equal(noneChip.className, 'filter-none');
   assert.equal(noneChip.textContent, Strings.map.transportationRoute.none);
});


test('Test_CreateFilterChip_TestLabel_ExpectChip', () => {
   const label = 'Animals';

   const chip = ExploreFilterBinder.createFilterChip(label);

   assert.equal(chip.className, 'filter-chip');
   assert.equal(chip.textContent, label);
});


test('Test_GetSelectedTypeValues_TestNoneRoute_ExpectCheckedOnly', () => {
   const animal = _createCheckbox(ItemType.ANIMAL, { checked: true });
   const restaurant = _createCheckbox(ItemType.RESTAURANT, { checked: false });

   const values = ExploreFilterBinder.getSelectedTypeValues([animal, restaurant], 'none');

   assert.deepEqual(values, [ItemType.ANIMAL]);
});


test('Test_GetSelectedTypeValues_TestSummerRoute_ExpectIncludesTransportation', () => {
   const animal = _createCheckbox(ItemType.ANIMAL, { checked: true });
   const restaurant = _createCheckbox(ItemType.RESTAURANT, { checked: false });
   const route = 'summer';

   const values = ExploreFilterBinder.getSelectedTypeValues([animal, restaurant], route);

   assert.deepEqual(values, [ItemType.ANIMAL, ItemType.TRANSPORTATION_ROUTE]);
});


test('Test_RenderSelectedChips_TestEmpty_ExpectNoneChip', () => {
   const chipContainer = document.createElement('div');
   const animal = _createCheckbox(ItemType.ANIMAL, { checked: false, label: 'Animals' });

   ExploreFilterBinder.renderSelectedChips(chipContainer, [animal]);

   assert.equal(chipContainer.children.at(Position.FIRST).className, 'filter-none');
});


test('Test_RenderSelectedChips_TestSelected_ExpectChip', () => {
   const chipContainer = document.createElement('div');
   const label = 'Animals';
   const animal = _createCheckbox(ItemType.ANIMAL, { checked: true, label });

   ExploreFilterBinder.renderSelectedChips(chipContainer, [animal]);

   assert.equal(chipContainer.children.at(Position.FIRST).className, 'filter-chip');
   assert.equal(chipContainer.children.at(Position.FIRST).textContent, label);
});


test('Test_RenderSelectedChips_TestMissingContainer_ExpectNoOp', () => {
   const animal = _createCheckbox(ItemType.ANIMAL, { checked: true, label: 'Animals' });

   const render = () => ExploreFilterBinder.renderSelectedChips(null, [animal]);

   assert.doesNotThrow(render);
});


test('Test_CreateExploreFilterState_TestSelection_ExpectFlags', () => {
   const original = ExploreFilter.buildExploreSearchIncludeFlags;
   const route = 'summer';
   ExploreFilter.buildExploreSearchIncludeFlags = (types, nextRoute) => ({ types, route: nextRoute });

   try {
      const animal = _createCheckbox(ItemType.ANIMAL, { checked: true });
      const state = ExploreFilterBinder.createExploreFilterState({
         checkboxes: [animal],
         getTransportationRoute: () => route,
      });

      assert.deepEqual(state.getSelectedTypes(), [ItemType.ANIMAL, ItemType.TRANSPORTATION_ROUTE]);
      assert.deepEqual(state.buildSearchIncludeFlags(), {
         types: [ItemType.ANIMAL, ItemType.TRANSPORTATION_ROUTE],
         route,
      });
   } finally {
      ExploreFilter.buildExploreSearchIncludeFlags = original;
   }
});


test('Test_BindDropdownEvents_TestOpenClose_ExpectToggle', () => {
   const multiSelect = document.createElement('div');
   _patchToggle(multiSelect);
   const button = document.createElement('button');
   const dropdown = document.createElement('div');
   const documentListeners = {};
   const originalAdd = document.addEventListener;
   document.addEventListener = (eventName, handler) => {
      documentListeners[eventName] = handler;
   };

   try {
      ExploreFilterBinder.bindDropdownEvents({ multiSelect, button, dropdown });
      button.listeners.click({ stopPropagation() {} });
      const opened = multiSelect.classList.contains('open');
      dropdown.listeners.click({ stopPropagation() {} });
      documentListeners.click();
      const closed = multiSelect.classList.contains('open');

      assert.equal(opened, true);
      assert.equal(closed, false);
   } finally {
      document.addEventListener = originalAdd;
   }
});


test('Test_BindCheckboxEvents_TestChange_ExpectCallbacks', () => {
   const checkbox = _createCheckbox(ItemType.ANIMAL, { checked: true });
   const changes = [];
   const unchecked = [];
   const selectionChanged = [];

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
});
