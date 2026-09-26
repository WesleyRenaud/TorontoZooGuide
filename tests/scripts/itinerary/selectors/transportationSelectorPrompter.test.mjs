import assert from 'node:assert/strict';
import test from 'node:test';

import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { TransportationSelectorPrompter } from '../../../../scripts/itinerary/selectors/transportationSelectorPrompter.js';
import { TransportationSelectorModel } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_PromptForAddAsTransportationSelection_TestRow_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMessage = TransportationSelectorModel.buildAddAsTransportationMessage;
   const message = 'Add Zoomobile?';
   const proceed = () => {};
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   TransportationSelectorModel.buildAddAsTransportationMessage = () => message;

   try {
      TransportationSelectorPrompter.promptForAddAsTransportationSelection({ name: 'Zoomobile' }, proceed);

      assert.equal(calls.length, 1);
      assert.equal(calls.at(Position.FIRST).title, Strings.itinerary.confirmation.addAsTransportationTitle);
      assert.equal(calls.at(Position.FIRST).message, message);
      assert.equal(calls.at(Position.FIRST).confirmText, Strings.itinerary.actions.confirm);
      assert.equal(calls.at(Position.FIRST).onConfirm, proceed);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      TransportationSelectorModel.buildAddAsTransportationMessage = originalMessage;
   }
});
