import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelectorRenderer } from '../../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorRenderer.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
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

   const wrap = bodyEl.children.at(Position.FIRST);
   assert.equal(wrap.className, 'itin-selector-toggle-wrap');
   const checkbox = wrap.children.at(Position.FIRST).children.at(Position.FIRST);
   checkbox.checked = true;
   checkbox.listeners.change?.();
   assert.equal(checkedValue, true);
   assert.equal(rerunCount, 1);
});
