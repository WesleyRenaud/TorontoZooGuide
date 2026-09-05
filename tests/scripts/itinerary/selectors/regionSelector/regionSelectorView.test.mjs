import assert from 'node:assert/strict';
import { test } from 'node:test';

import { View } from '../../../../../scripts/itinerary/selectors/regionSelector/view.js';
import { APP_STRINGS } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { dispatchResultsClick } from '../../../helpers/regionSelectorDom.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

test.describe('region selector view', () => {
   installDomTestHooks();

   test('Test_RenderRegionSelectionView_TestRenderRegionSelectionViewNoOpsWhenResultsElIsMissing_ExpectOk', () => {
      View.renderRegionSelectionView(null, [{ name: 'Africa', exhibits: ['Africa Savanna'] }], []);
   });

   test('Test_RenderRegionSelectionView_TestRenderRegionSelectionViewShowsTheEmptyStateWhenNoRegions_ExpectOk', () => {
      const resultsEl = createDomNode('div', 'itin-results');

      View.renderRegionSelectionView(resultsEl, [], []);

      assert.equal(resultsEl.children.length, 1);
      assert.equal(resultsEl.children[0].className, 'itin-empty');
      assert.equal(
         resultsEl.children[0].textContent,
         APP_STRINGS.itinerary.emptyText.regions
      );
   });

   test('Test_RenderRegionSelectionView_TestRenderRegionSelectionViewRendersRegionAndExhibitChoiceRows_ExpectOk', () => {
      const resultsEl = createDomNode('div', 'itin-results');

      View.renderRegionSelectionView(
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

   test('Test_BindRegionSelectionEvents_TestBindRegionSelectionEventsRoutesRegionAndExhibitToggleClicks_ExpectOk', () => {
      const resultsEl = createDomNode('div', 'itin-results');
      const regionCalls = [];
      const exhibitCalls = [];

      View.bindRegionSelectionEvents(resultsEl, {
         onToggleRegion: (regionName) => {
            regionCalls.push(regionName);
         },
         onToggleExhibit: (regionName, exhibitName) => {
            exhibitCalls.push({ regionName, exhibitName });
         },
      });

      View.renderRegionSelectionView(
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

   test('Test_BindRegionSelectionEvents_TestBindRegionSelectionEventsNoOpsWhenResultsElIsMissing_ExpectOk', () => {
      View.bindRegionSelectionEvents(null, {
         onToggleRegion: () => {
            assert.fail('should not register listeners');
         },
      });
   });

   test('Test_BindRegionSelectionEvents_TestBindRegionSelectionEventsIgnoresClicksOutsideActionableButtons_ExpectOk', () => {
      const resultsEl = createDomNode('div', 'itin-results');
      const regionCalls = [];

      View.bindRegionSelectionEvents(resultsEl, {
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
