import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionSelectorPrompter } from '../../../../scripts/itinerary/selectors/attractionSelectorPrompter.js';
import { AttractionSelectorModel } from '../../../../scripts/itinerary/selectors/attractionSelector/attractionSelectorModel.js';
import { ConfirmFragment } from '../../../../scripts/itinerary/panel/components/confirmFragment.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_PromptForClosedAttractionSelection_TestRow_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMessage = AttractionSelectorModel.buildClosedAttractionMessage;
   const message = 'May be closed';
   const proceed = () => {};
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   AttractionSelectorModel.buildClosedAttractionMessage = () => message;

   try {
      AttractionSelectorPrompter.promptForClosedAttractionSelection({ name: 'Carousel' }, proceed);

      assert.equal(calls.at(Position.FIRST).title, Strings.itinerary.confirmation.attractionMayBeClosed);
      assert.equal(calls.at(Position.FIRST).message, message);
      assert.equal(calls.at(Position.FIRST).onConfirm, proceed);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      AttractionSelectorModel.buildClosedAttractionMessage = originalMessage;
   }
});


test('Test_PromptForAlsoTransportationAttractionSelection_TestRow_ExpectPopup', () => {
   const calls = [];
   const originalShow = ConfirmFragment.showItineraryConfirmPopup;
   const originalMessage = AttractionSelectorModel.buildAlsoTransportationAttractionMessage;
   const message = 'Also transportation';
   ConfirmFragment.showItineraryConfirmPopup = (args) => { calls.push(args); };
   AttractionSelectorModel.buildAlsoTransportationAttractionMessage = () => message;

   try {
      AttractionSelectorPrompter.promptForAlsoTransportationAttractionSelection({ name: 'Zoomobile' }, () => {});

      assert.equal(
         calls.at(Position.FIRST).title,
         Strings.itinerary.confirmation.attractionAlsoTransportationTitle
      );
      assert.equal(calls.at(Position.FIRST).message, message);
   } finally {
      ConfirmFragment.showItineraryConfirmPopup = originalShow;
      AttractionSelectorModel.buildAlsoTransportationAttractionMessage = originalMessage;
   }
});
