import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { TransportationSelectorPrompter } from '../../../../scripts/itinerary/selectors/transportationSelectorPrompter.js';
import { TransportationSelectorModel } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_PromptForAddAsTransportationSelection_TestRow_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMessage = TransportationSelectorModel.buildAddAsTransportationMessage;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   TransportationSelectorModel.buildAddAsTransportationMessage = () => 'Add Zoomobile?';

   try {
      const proceed = () => {};
      TransportationSelectorPrompter.promptForAddAsTransportationSelection({ name: 'Zoomobile' }, proceed);
      assert.equal(calls.length, 1);
      assert.equal(calls[0].title, Strings.itinerary.confirmation.addAsTransportationTitle);
      assert.equal(calls[0].message, 'Add Zoomobile?');
      assert.equal(calls[0].confirmText, Strings.itinerary.actions.confirm);
      assert.equal(calls[0].onConfirm, proceed);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      TransportationSelectorModel.buildAddAsTransportationMessage = originalMessage;
   }
});
