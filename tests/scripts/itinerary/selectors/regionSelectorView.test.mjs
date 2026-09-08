import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionSelectorView } from '../../../../scripts/itinerary/selectors/regionSelectorView.js';
import { RegionSelectorShellBuilder } from '../../../../scripts/itinerary/selectors/regionSelector/regionSelectorShellBuilder.js';

test('Test_CreateRegionSelectorElements_TestShell_ExpectMappedParts', () => {
   const original = RegionSelectorShellBuilder.buildRegionSelectorShell;
   RegionSelectorShellBuilder.buildRegionSelectorShell = () => ({
      root: { id: 'root' },
      resultsEl: { id: 'results' },
      prevButton: { id: 'prev' },
      nextButton: { id: 'next' },
      finishButton: { id: 'finish' },
      closeButton: { id: 'close' },
   });

   try {
      assert.deepEqual(RegionSelectorView.createRegionSelectorElements(), {
         rootEl: { id: 'root' },
         resultsEl: { id: 'results' },
         prevButtonEl: { id: 'prev' },
         nextButtonEl: { id: 'next' },
         finishButtonEl: { id: 'finish' },
         closeButtonEl: { id: 'close' },
      });
   } finally {
      RegionSelectorShellBuilder.buildRegionSelectorShell = original;
   }
});
