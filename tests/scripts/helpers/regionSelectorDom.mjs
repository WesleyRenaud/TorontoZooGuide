import assert from 'node:assert/strict';

export function findChoiceButton(root, { action, exhibitName = '', regionName = '' } = {}) {
   const stack = [root];

   while (stack.length > 0) {
      const node = stack.shift();

      if (
         node.dataset?.action === action
         && (!exhibitName || node.dataset.exhibit === exhibitName)
         && (!regionName || node.dataset.region === regionName)
      ) {
         return node;
      }

      stack.push(...(node.children ?? []));
   }

   return null;
}

export function dispatchResultsClick(resultsEl, button) {
   resultsEl.listeners.click({
      target: button,
      preventDefault() {},
      stopPropagation() {},
   });
}

export function clickExhibitToggle(resultsEl, exhibitName) {
   const button = findChoiceButton(resultsEl, {
      action: 'toggle-exhibit',
      exhibitName,
   });

   assert.ok(button, `Expected exhibit toggle for ${exhibitName}`);

   dispatchResultsClick(resultsEl, button);
}

export function clickRegionToggle(resultsEl, regionName) {
   const button = findChoiceButton(resultsEl, {
      action: 'toggle-region',
      regionName,
   });

   assert.ok(button, `Expected region toggle for ${regionName}`);

   dispatchResultsClick(resultsEl, button);
}
