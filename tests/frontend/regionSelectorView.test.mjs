import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import {
   bindRegionSelectionEvents,
   renderRegionSelectionView,
} from '../../scripts/itinerary/selectors/regionSelector/view.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { createDomNode } from './helpers/domNodeMock.mjs';
import { installDocument, installTestWindow, teardownDocument } from './helpers/domMock.mjs';

function dispatchResultsClick(resultsEl, button) {
   resultsEl.listeners.click({
      target: button,
      preventDefault() {},
      stopPropagation() {},
   });
}

test.describe('region selector view', () => {
   beforeEach(() => {
      installTestWindow();
      installDocument();
   });

   afterEach(() => {
      teardownDocument();
      delete globalThis.window;
   });

   test('renderRegionSelectionView no-ops when resultsEl is missing', () => {
      renderRegionSelectionView(null, [{ name: 'Africa', exhibits: ['Africa Savanna'] }], []);
   });

   test('renderRegionSelectionView shows the empty state when no regions are available', () => {
      const resultsEl = createDomNode('div', 'itin-results');

      renderRegionSelectionView(resultsEl, [], []);

      assert.equal(resultsEl.children.length, 1);
      assert.equal(resultsEl.children[0].className, 'itin-empty');
      assert.equal(
         resultsEl.children[0].textContent,
         APP_STRINGS.itinerary.emptyText.regions
      );
   });

   test('renderRegionSelectionView renders region and exhibit choice rows', () => {
      const resultsEl = createDomNode('div', 'itin-results');

      renderRegionSelectionView(
         resultsEl,
         [{ name: 'Africa', exhibits: ['Africa Savanna', 'Indoor Rainforest'] }],
         new Set(['Africa Savanna'])
      );

      const buttons = resultsEl.querySelectorAll('.itin-region-choice-row');

      assert.equal(buttons.length, 3);
      assert.equal(buttons[0].dataset.action, 'toggle-region');
      assert.equal(buttons[0].dataset.region, 'Africa');
      assert.equal(buttons[1].dataset.action, 'toggle-exhibit');
      assert.equal(buttons[1].dataset.exhibit, 'Africa Savanna');
   });

   test('bindRegionSelectionEvents routes region and exhibit toggle clicks', () => {
      const resultsEl = createDomNode('div', 'itin-results');
      const regionCalls = [];
      const exhibitCalls = [];

      bindRegionSelectionEvents(resultsEl, {
         onToggleRegion: (regionName) => {
            regionCalls.push(regionName);
         },
         onToggleExhibit: (regionName, exhibitName) => {
            exhibitCalls.push({ regionName, exhibitName });
         },
      });

      renderRegionSelectionView(
         resultsEl,
         [{ name: 'Africa', exhibits: ['Africa Savanna'] }],
         new Set()
      );

      const [regionButton, exhibitButton] = resultsEl.querySelectorAll('.itin-region-choice-row');

      dispatchResultsClick(resultsEl, regionButton);
      dispatchResultsClick(resultsEl, exhibitButton);

      assert.deepEqual(regionCalls, ['Africa']);
      assert.deepEqual(exhibitCalls, [{
         regionName: 'Africa',
         exhibitName: 'Africa Savanna',
      }]);
   });

   test('bindRegionSelectionEvents no-ops when resultsEl is missing', () => {
      bindRegionSelectionEvents(null, {
         onToggleRegion: () => {
            assert.fail('should not register listeners');
         },
      });
   });

   test('bindRegionSelectionEvents ignores clicks outside actionable buttons', () => {
      const resultsEl = createDomNode('div', 'itin-results');
      const regionCalls = [];

      bindRegionSelectionEvents(resultsEl, {
         onToggleRegion: (regionName) => {
            regionCalls.push(regionName);
         },
      });

      const label = createDomNode('div', 'itin-panel-name', 'Africa');
      resultsEl.appendChild(label);

      dispatchResultsClick(resultsEl, label);

      assert.deepEqual(regionCalls, []);
   });
});
