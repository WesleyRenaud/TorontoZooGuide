import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { ScheduleItemConfirmationController } from '../../../../scripts/itinerary/panel/scheduleItemConfirmationController.js';
import { ScheduleItemConfirmationFlowHelper } from '../../../../scripts/itinerary/panel/scheduleItemConfirmationFlowHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_GetConfirmationMountEl_TestMissingPanel_ExpectBody', () => {
   const original = ItineraryPanelFragment.getItineraryPanelMountEl;
   ItineraryPanelFragment.getItineraryPanelMountEl = () => null;

   try {
      const mountEl = ScheduleItemConfirmationFlowHelper.getConfirmationMountEl();

      assert.equal(mountEl, document.body);
   } finally {
      ItineraryPanelFragment.getItineraryPanelMountEl = original;
   }
});


test('Test_GetConfirmationMountEl_TestPanel_ExpectMount', () => {
   const original = ItineraryPanelFragment.getItineraryPanelMountEl;
   const mount = document.createElement('div');
   ItineraryPanelFragment.getItineraryPanelMountEl = () => mount;

   try {
      const mountEl = ScheduleItemConfirmationFlowHelper.getConfirmationMountEl();

      assert.equal(mountEl, mount);
   } finally {
      ItineraryPanelFragment.getItineraryPanelMountEl = original;
   }
});


test('Test_RequestScheduleItemConfirmation_TestConfirm_ExpectConfirmedResult', async () => {
   const original = ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation;
   const scheduled = { ok: true };
   ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = async () => scheduled;

   try {
      const result = await ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
         showConfirmation: ({ onConfirm }) => onConfirm({ note: 'yes' }),
         initialResult: { draft: true },
         request: { id: 1 },
         confirmationOptions: { a: 1 },
         buildConfirmedOptions: (args) => ({ confirmedNote: args.note }),
      });

      assert.deepEqual(result, scheduled);
   } finally {
      ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = original;
   }
});


test('Test_RequestScheduleItemConfirmation_TestCancel_ExpectCancelled', async () => {
   const initialResult = { draft: true };

   const result = await ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
      showConfirmation: ({ onCancel }) => onCancel(),
      initialResult,
      request: {},
      confirmationOptions: {},
      buildConfirmedOptions: () => ({}),
   });

   assert.deepEqual(result, { ...initialResult, cancelled: true });
});


test('Test_RequestScheduleItemConfirmation_TestConfirmErrorAsSaveFailed_ExpectFailedResult', async () => {
   const originalSchedule = ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation;
   const originalFailed = ScheduleItemConfirmationController.createScheduleItemSaveFailedResult;
   const failed = { failed: true };
   ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = async () => {
      throw new Error('boom');
   };
   ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = () => failed;

   try {
      const result = await ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
         showConfirmation: ({ onConfirm }) => onConfirm({}),
         initialResult: {},
         request: {},
         confirmationOptions: {},
         buildConfirmedOptions: () => ({}),
         resolveConfirmErrorAsSaveFailed: true,
      });

      assert.deepEqual(result, failed);
   } finally {
      ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = originalSchedule;
      ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = originalFailed;
   }
});
