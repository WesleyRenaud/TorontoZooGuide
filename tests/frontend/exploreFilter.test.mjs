import assert from 'node:assert/strict';
import test from 'node:test';

import {
   buildExploreSearchIncludeFlags,
   initExploreTypeFilter,
} from '../../scripts/search/exploreFilter.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

function createCheckboxOption({ value, label, checked = false }) {
   const labelEl = createDomNode('label');
   const checkbox = createDomNode('input');

   checkbox.type = 'checkbox';
   checkbox.value = value;
   checkbox.checked = checked;
   labelEl.textContent = label;
   labelEl.appendChild(checkbox);
   checkbox.closest = (selector) => (
      selector === 'label' ? labelEl : null
   );
   checkbox.dispatchChange = () => {
      checkbox.listeners.change?.();
   };

   return { checkbox, labelEl };
}

function createExploreTypeFilterDom({
   selected = [],
} = {}) {
   const multiSelect = createDomNode('div', 'multi-select');
   const button = createDomNode('button', 'multi-select-button');
   const dropdown = createDomNode('div', 'multi-select-dropdown');
   const chipContainer = createDomNode('div', 'selected-values');
   const options = [
      { value: 'animal', label: 'Animals' },
      { value: 'restaurant', label: 'Restaurants' },
   ];
   const checkboxes = options.map((option) => {
      const { checkbox, labelEl } = createCheckboxOption({
         value: option.value,
         label: option.label,
         checked: selected.includes(option.value),
      });

      dropdown.appendChild(labelEl);

      return checkbox;
   });

   dropdown.querySelectorAll = (selector) => (
      selector === 'input[type="checkbox"]' ? checkboxes : []
   );
   multiSelect.appendChild(button);
   multiSelect.appendChild(dropdown);
   multiSelect.appendChild(chipContainer);
   multiSelect.classList.toggle = (className, shouldAdd) => {
      if (shouldAdd) {
         multiSelect.classList.add(className);
      }
      else {
         multiSelect.classList.delete(className);
      }
   };

   return {
      multiSelect,
      button,
      dropdown,
      chipContainer,
      checkboxes,
   };
}

test('buildExploreSearchIncludeFlags maps selected explore types to search flags', () => {
   assert.deepEqual(
      buildExploreSearchIncludeFlags(['animal', 'restaurant', 'wildEncounter'], 'none'),
      {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: true,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: true,
         includeZoomobileStations: false,
      }
   );
});

test('buildExploreSearchIncludeFlags includes zoomobile stations when a route is selected', () => {
   assert.deepEqual(
      buildExploreSearchIncludeFlags(['animal'], 'current'),
      {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: false,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: false,
         includeZoomobileStations: true,
         zoomobileRoute: 'current',
      }
   );
});

test('initExploreTypeFilter returns fallback state when type filter is missing', () => {
   installTestWindow();
   installDocument();

   try {
      const filter = initExploreTypeFilter({
         multiSelect: null,
      });

      assert.deepEqual(filter.getSelectedTypes(), ['animal']);
      assert.deepEqual(filter.buildSearchIncludeFlags(), {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: false,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: false,
         includeZoomobileStations: false,
      });
   }
   finally {
      teardownDocument();
   }
});

test('initExploreTypeFilter tracks checkbox selection and zoomobile route', () => {
   installTestWindow();
   installDocument();

   try {
      const changeCalls = [];
      const animalsUncheckedCalls = [];
      const { multiSelect, checkboxes, chipContainer } = createExploreTypeFilterDom({
         selected: ['animal'],
      });

      const filter = initExploreTypeFilter({
         multiSelect,
         getZoomobileRoute: () => 'current',
         onChange: () => {
            changeCalls.push('changed');
         },
         onAnimalsUnchecked: () => {
            animalsUncheckedCalls.push('unchecked');
         },
      });

      assert.deepEqual(filter.getSelectedTypes(), ['animal', 'zoomobileRoute']);
      assert.deepEqual(filter.buildSearchIncludeFlags(), {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: false,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: false,
         includeZoomobileStations: true,
         zoomobileRoute: 'current',
      });
      assert.equal(chipContainer.children.length, 1);
      assert.equal(chipContainer.children[0].className, 'filter-chip');
      assert.equal(chipContainer.children[0].textContent, 'Animals');

      checkboxes[0].checked = false;
      checkboxes[0].dispatchChange();

      assert.deepEqual(filter.getSelectedTypes(), ['zoomobileRoute']);
      assert.deepEqual(changeCalls, ['changed']);
      assert.deepEqual(animalsUncheckedCalls, ['unchecked']);
      assert.equal(chipContainer.children[0].className, 'filter-none');
      assert.equal(
         chipContainer.children[0].textContent,
         APP_STRINGS.map.zoomobileRoute.none
      );

      checkboxes[1].checked = true;
      checkboxes[1].dispatchChange();

      assert.deepEqual(filter.getSelectedTypes(), ['restaurant', 'zoomobileRoute']);
      assert.deepEqual(changeCalls, ['changed', 'changed']);
      assert.equal(chipContainer.children[0].textContent, 'Restaurants');
   }
   finally {
      teardownDocument();
   }
});
