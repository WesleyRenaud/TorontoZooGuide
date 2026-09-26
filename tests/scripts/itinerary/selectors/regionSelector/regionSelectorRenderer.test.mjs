import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RegionSelectorRenderer } from '../../../../../scripts/itinerary/selectors/regionSelector/regionSelectorRenderer.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';
import { createDomNode } from '../../../helpers/domNodeMock.mjs';
import { dispatchResultsClick } from '../../../helpers/regionSelectorDom.mjs';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_RenderRegionSelectionView_TestMissingResultsEl_ExpectNoOp', () => {
   const regions = [{ name: 'Africa', exhibits: ['Africa Savanna'] }];

   RegionSelectorRenderer.renderRegionSelectionView(null, regions, []);
});


test('Test_RenderRegionSelectionView_TestNoRegions_ExpectEmptyState', () => {
   const resultsEl = createDomNode('div', 'itin-results');

   RegionSelectorRenderer.renderRegionSelectionView(resultsEl, [], []);

   assert.equal(resultsEl.children.length, 1);
   assert.equal(resultsEl.children.at(Position.FIRST).className, 'itin-empty');
   assert.equal(
      resultsEl.children.at(Position.FIRST).textContent,
      Strings.itinerary.emptyText.regions
   );
});


test('Test_RenderRegionSelectionView_TestRegionAndExhibits_ExpectChoiceRows', () => {
   const resultsEl = createDomNode('div', 'itin-results');
   const regionName = 'Africa';
   const savanna = 'Africa Savanna';
   const rainforest = 'Indoor Rainforest';

   RegionSelectorRenderer.renderRegionSelectionView(
      resultsEl,
      [{ name: regionName, exhibits: [savanna, rainforest] }],
      new Set([savanna])
   );

   const buttons = resultsEl.querySelectorAll('.itin-region-choice-row');
   assert.equal(buttons.length, 3);
   assert.equal(buttons[Position.FIRST].dataset.action, 'toggle-region');
   assert.equal(buttons[Position.FIRST].dataset.region, regionName);
   assert.equal(buttons[Position.SECOND].dataset.action, 'toggle-exhibit');
   assert.equal(buttons[Position.SECOND].dataset.exhibit, savanna);
});


test('Test_BindRegionSelectionEvents_TestToggles_ExpectRouted', () => {
   const resultsEl = createDomNode('div', 'itin-results');
   const regionCalls = [];
   const exhibitCalls = [];
   const regionName = 'Africa';
   const exhibitName = 'Africa Savanna';

   RegionSelectorRenderer.bindRegionSelectionEvents(resultsEl, {
      onToggleRegion: (name) => {
         regionCalls.push(name);
      },
      onToggleExhibit: (name, exhibit) => {
         exhibitCalls.push({ regionName: name, exhibitName: exhibit });
      },
   });
   RegionSelectorRenderer.renderRegionSelectionView(
      resultsEl,
      [{ name: regionName, exhibits: [exhibitName] }],
      new Set()
   );
   const [regionButton, exhibitButton] = resultsEl.querySelectorAll('.itin-region-choice-row');

   dispatchResultsClick(resultsEl, regionButton);
   dispatchResultsClick(resultsEl, exhibitButton);

   assert.deepEqual(regionCalls, [regionName]);
   assert.deepEqual(exhibitCalls, [{ regionName, exhibitName }]);
});


test('Test_BindRegionSelectionEvents_TestMissingResultsEl_ExpectNoOp', () => {
   RegionSelectorRenderer.bindRegionSelectionEvents(null, {
      onToggleRegion: () => {
         assert.fail('should not register listeners');
      },
   });
});


test('Test_BindRegionSelectionEvents_TestNonButtonClick_ExpectIgnored', () => {
   const resultsEl = createDomNode('div', 'itin-results');
   const regionCalls = [];
   const labelText = 'Africa';

   RegionSelectorRenderer.bindRegionSelectionEvents(resultsEl, {
      onToggleRegion: (regionName) => {
         regionCalls.push(regionName);
      },
   });
   const label = createDomNode('div', 'itin-panel-name', labelText);
   resultsEl.appendChild(label);

   dispatchResultsClick(resultsEl, label);

   assert.deepEqual(regionCalls, []);
});
