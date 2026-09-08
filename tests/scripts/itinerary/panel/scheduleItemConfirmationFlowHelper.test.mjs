import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelFragment } from '../../../../scripts/itinerary/panel/components/itineraryPanelFragment.js';
import { ScheduleItemConfirmationController } from '../../../../scripts/itinerary/panel/scheduleItemConfirmationController.js';
import { ScheduleItemConfirmationFlowHelper } from '../../../../scripts/itinerary/panel/scheduleItemConfirmationFlowHelper.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_GetConfirmationMountEl_TestPanelOrBody_ExpectMount', () => {
   const original = ItineraryPanelFragment.getItineraryPanelMountEl;
   ItineraryPanelFragment.getItineraryPanelMountEl = () => null;

   try {
      assert.equal(ScheduleItemConfirmationFlowHelper.getConfirmationMountEl(), document.body);
   } finally {
      ItineraryPanelFragment.getItineraryPanelMountEl = original;
   }

   const mount = document.createElement('div');
   ItineraryPanelFragment.getItineraryPanelMountEl = () => mount;
   try {
      assert.equal(ScheduleItemConfirmationFlowHelper.getConfirmationMountEl(), mount);
   } finally {
      ItineraryPanelFragment.getItineraryPanelMountEl = original;
   }
});

test('Test_RequestScheduleItemConfirmation_TestConfirm_ExpectConfirmedResult', async () => {
   const original = ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation;
   ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = async () => ({
      ok: true,
   });

   try {
      const result = await ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
         showConfirmation: ({ onConfirm }) => onConfirm({ note: 'yes' }),
         initialResult: { draft: true },
         request: { id: 1 },
         confirmationOptions: { a: 1 },
         buildConfirmedOptions: (args) => ({ confirmedNote: args.note }),
      });

      assert.deepEqual(result, { ok: true });
   } finally {
      ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = original;
   }
});

test('Test_RequestScheduleItemConfirmation_TestCancel_ExpectCancelled', async () => {
   const result = await ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
      showConfirmation: ({ onCancel }) => onCancel(),
      initialResult: { draft: true },
      request: {},
      confirmationOptions: {},
      buildConfirmedOptions: () => ({}),
   });

   assert.deepEqual(result, { draft: true, cancelled: true });
});

test('Test_RequestScheduleItemConfirmation_TestConfirmErrorAsSaveFailed_ExpectFailedResult', async () => {
   const originalSchedule = ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation;
   const originalFailed = ScheduleItemConfirmationController.createScheduleItemSaveFailedResult;
   ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = async () => {
      throw new Error('boom');
   };
   ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = () => ({ failed: true });

   try {
      const result = await ScheduleItemConfirmationFlowHelper.requestScheduleItemConfirmation({
         showConfirmation: ({ onConfirm }) => onConfirm({}),
         initialResult: {},
         request: {},
         confirmationOptions: {},
         buildConfirmedOptions: () => ({}),
         resolveConfirmErrorAsSaveFailed: true,
      });

      assert.deepEqual(result, { failed: true });
   } finally {
      ScheduleItemConfirmationController.scheduleItineraryItemWithConfirmation = originalSchedule;
      ScheduleItemConfirmationController.createScheduleItemSaveFailedResult = originalFailed;
   }
});
