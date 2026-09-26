import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionSelectorView } from '../../../../scripts/itinerary/selectors/regionSelectorView.js';
import { RegionSelectorShellBuilder } from '../../../../scripts/itinerary/selectors/regionSelector/regionSelectorShellBuilder.js';


test('Test_CreateRegionSelectorElements_TestShell_ExpectMappedParts', () => {
   const original = RegionSelectorShellBuilder.buildRegionSelectorShell;
   const root = { id: 'root' };
   const results = { id: 'results' };
   const prev = { id: 'prev' };
   const next = { id: 'next' };
   const finish = { id: 'finish' };
   const close = { id: 'close' };
   RegionSelectorShellBuilder.buildRegionSelectorShell = () => ({
      root,
      resultsEl: results,
      prevButton: prev,
      nextButton: next,
      finishButton: finish,
      closeButton: close,
   });

   try {
      const elements = RegionSelectorView.createRegionSelectorElements();

      assert.equal(elements.rootEl, root);
      assert.equal(elements.resultsEl, results);
      assert.equal(elements.prevButtonEl, prev);
      assert.equal(elements.nextButtonEl, next);
      assert.equal(elements.finishButtonEl, finish);
      assert.equal(elements.closeButtonEl, close);
   } finally {
      RegionSelectorShellBuilder.buildRegionSelectorShell = original;
   }
});
