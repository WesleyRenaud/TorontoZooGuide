import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelectorPrompter } from '../../../../scripts/itinerary/selectors/attractionSelectorPrompter.js';
import { AttractionSelectorModel } from '../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_PromptForClosedAttractionSelection_TestRow_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMessage = AttractionSelectorModel.buildClosedAttractionMessage;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   AttractionSelectorModel.buildClosedAttractionMessage = () => 'May be closed';

   try {
      const proceed = () => {};
      AttractionSelectorPrompter.promptForClosedAttractionSelection({ name: 'Carousel' }, proceed);
      assert.equal(calls[0].title, Strings.itinerary.confirmation.attractionMayBeClosed);
      assert.equal(calls[0].message, 'May be closed');
      assert.equal(calls[0].onConfirm, proceed);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      AttractionSelectorModel.buildClosedAttractionMessage = originalMessage;
   }
});

test('Test_PromptForAlsoTransportationAttractionSelection_TestRow_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMessage = AttractionSelectorModel.buildAlsoTransportationAttractionMessage;
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   AttractionSelectorModel.buildAlsoTransportationAttractionMessage = () => 'Also transportation';

   try {
      AttractionSelectorPrompter.promptForAlsoTransportationAttractionSelection({ name: 'Zoomobile' }, () => {});
      assert.equal(calls[0].title, Strings.itinerary.confirmation.attractionAlsoTransportationTitle);
      assert.equal(calls[0].message, 'Also transportation');
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      AttractionSelectorModel.buildAlsoTransportationAttractionMessage = originalMessage;
   }
});
