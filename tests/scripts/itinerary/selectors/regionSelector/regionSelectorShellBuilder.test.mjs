import assert from 'node:assert/strict';
import test from 'node:test';

import { RegionSelectorShellBuilder } from '../../../../../scripts/itinerary/selectors/regionSelector/regionSelectorShellBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BuildRegionSelectorShell_TestDefaults_ExpectShellParts', () => {
   const shell = RegionSelectorShellBuilder.buildRegionSelectorShell();

   assert.equal(shell.root.className, 'itin-overlay');
   assert.equal(shell.resultsEl.className, 'itin-region-results itin-results');
   assert.equal(shell.prevButton.textContent, Strings.animalsPage.back);
   assert.equal(shell.nextButton.textContent, Strings.itinerary.actions.next);
   assert.equal(shell.finishButton.textContent, Strings.itinerary.actions.finish);
   assert.match(shell.root.textContent, new RegExp(Strings.itinerary.selectors.titleRegions));
});
