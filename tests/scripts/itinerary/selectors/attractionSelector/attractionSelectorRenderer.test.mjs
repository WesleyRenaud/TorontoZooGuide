import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelectorRenderer } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorRenderer.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_RenderIncludeClosedAttractionsToggle_TestChange_ExpectCallbacks', () => {
   const bodyEl = document.createElement('div');
   bodyEl.insertBefore = (node, referenceNode) => {
      const index = bodyEl.children.indexOf(referenceNode);
      if (index >= 0) {
         bodyEl.children.splice(index, 0, node);
      } else {
         bodyEl.children.unshift(node);
      }
      node.parentElement = bodyEl;
      return node;
   };
   const search = document.createElement('input');
   search.className = 'itin-search-input';
   bodyEl.appendChild(search);

   let checkedValue = null;
   let rerunCount = 0;

   AttractionSelectorRenderer.renderIncludeClosedAttractionsToggle({
      bodyEl,
      onChange: (checked) => { checkedValue = checked; },
      rerunSearch: () => { rerunCount += 1; },
   });

   assert.equal(bodyEl.children[0].className, 'itin-selector-toggle-wrap');
   const checkbox = bodyEl.children[0].children[0].children[0];
   checkbox.checked = true;
   checkbox.listeners.change?.();
   assert.equal(checkedValue, true);
   assert.equal(rerunCount, 1);
});
