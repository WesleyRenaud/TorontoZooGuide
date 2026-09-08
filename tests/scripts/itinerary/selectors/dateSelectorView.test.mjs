import assert from 'node:assert/strict';
import test from 'node:test';

import { DateSelectorView } from '../../../../scripts/itinerary/selectors/dateSelectorView.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BuildDateSelectorView_TestDefaultStrings_ExpectDialogParts', () => {
   const view = DateSelectorView.buildDateSelectorView();

   assert.equal(view.root.className, 'itin-overlay');
   assert.equal(view.root.querySelector('.itin-card').getAttribute('role'), 'dialog');
   assert.equal(view.root.querySelector('.itin-h1').textContent, Strings.itinerary.selectors.titleDate);
   assert.equal(view.inputEl.className, 'itin-date-input');
   assert.equal(view.inputEl.readOnly, true);
   assert.equal(view.nextButtonEl.textContent, Strings.itinerary.actions.next);
   assert.equal(view.finishButtonEl.textContent, Strings.itinerary.actions.finish);
   assert.equal(view.closeButtonEl.getAttribute('aria-label'), Strings.itinerary.aria.closeBuilder);
});
