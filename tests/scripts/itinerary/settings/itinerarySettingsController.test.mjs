import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySettingsController } from '../../../../scripts/itinerary/settings/itinerarySettingsController.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

function _checkbox(status, checked) {
   return {
      checked,
      dataset: { status },
   };
}

installDomTestHooks();


test('Test_CreateItinerarySettingsController_TestGearClick_ExpectSuppressableStatuses', async () => {
   const overlays = [];
   const gearEl = document.createElement('button');
   const mountEl = document.getElementById('itineraryFlow');
   const itemStatus = {
      status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      isSuppressable: true,
      isSuppressed: true,
   };
   const arrivalStatus = {
      status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
      isSuppressable: true,
      isSuppressed: false,
   };

   ItinerarySettingsController.createItinerarySettingsController({
      gearEl,
      mountEl,
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: ItineraryErrorType.SAVE_FAILED,
                  isSuppressable: false,
                  isSuppressed: false,
               },
               itemStatus,
               arrivalStatus,
            ],
         },
      }),
      showOverlay: (args) => {
         overlays.push(args);
      },
   });

   await gearEl.listeners.click();

   assert.equal(overlays.length, 1);
   assert.equal(overlays[Position.FIRST].mountEl, mountEl);
   assert.deepEqual(
      overlays[Position.FIRST].statuses.map((entry) => entry.status),
      [
         arrivalStatus.status,
         itemStatus.status,
      ]
   );
});


test('Test_CreateItinerarySettingsController_TestSave_ExpectPersistAndClose', async () => {
   const persistCalls = [];
   const closes = [];
   const closed = true;
   const suppressAction = 'suppress';
   const unsuppressAction = 'unsuppress';
   const arrivalStatus = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   const itemStatus = ItineraryErrorType.ITEM_NOT_ON_ITINERARY;
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      gearEl: document.createElement('button'),
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: arrivalStatus,
                  isSuppressable: true,
                  isSuppressed: false,
               },
               {
                  status: itemStatus,
                  isSuppressable: true,
                  isSuppressed: true,
               },
            ],
         },
      }),
      persistSuppression: async (status) => {
         persistCalls.push({ action: suppressAction, status });
      },
      persistUnsuppression: async (status) => {
         persistCalls.push({ action: unsuppressAction, status });
      },
      showOverlay: (args) => {
         overlayArgs = args;
      },
   });

   await control.open();
   await overlayArgs.onSave({
      close: () => {
         closes.push(closed);
      },
      view: {
         checkboxEls: [
            _checkbox(arrivalStatus, false),
            _checkbox(itemStatus, true),
         ],
      },
   });

   assert.deepEqual(persistCalls, [
      {
         action: suppressAction,
         status: arrivalStatus,
      },
      {
         action: unsuppressAction,
         status: itemStatus,
      },
   ]);
   assert.deepEqual(closes, [closed]);
});


test('Test_CreateItinerarySettingsController_TestSaveUnchanged_ExpectClosesWithoutPersist', async () => {
   const persistCalls = [];
   const closes = [];
   const closed = true;
   const arrivalStatus = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: arrivalStatus,
                  isSuppressable: true,
                  isSuppressed: false,
               },
            ],
         },
      }),
      persistSuppression: async (status) => {
         persistCalls.push(status);
      },
      showOverlay: (args) => {
         overlayArgs = args;
      },
   });

   await control.open();
   await overlayArgs.onSave({
      close: () => {
         closes.push(closed);
      },
      view: {
         checkboxEls: [
            _checkbox(arrivalStatus, true),
         ],
      },
   });

   assert.deepEqual(persistCalls, []);
   assert.deepEqual(closes, [closed]);
});


test('Test_CreateItinerarySettingsController_TestSaveThrows_ExpectStaysOpen', async () => {
   const closes = [];
   const arrivalStatus = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: arrivalStatus,
                  isSuppressable: true,
                  isSuppressed: false,
               },
            ],
         },
      }),
      persistSuppression: async () => {
         throw new Error('save failed');
      },
      showOverlay: (args) => {
         overlayArgs = args;
      },
   });

   await control.open();
   await overlayArgs.onSave({
      close: () => {
         closes.push(true);
      },
      view: {
         checkboxEls: [
            _checkbox(arrivalStatus, false),
         ],
      },
   });

   assert.deepEqual(closes, []);
});


test('Test_CreateItinerarySettingsController_TestCloseWithoutChanges_ExpectCloses', async () => {
   const confirms = [];
   const closes = [];
   const closed = true;
   const arrivalStatus = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: arrivalStatus,
                  isSuppressable: true,
                  isSuppressed: false,
               },
            ],
         },
      }),
      showConfirmPopup: (args) => {
         confirms.push(args);
      },
      showOverlay: (args) => {
         overlayArgs = args;
      },
   });

   await control.open();
   overlayArgs.onClose({
      close: () => {
         closes.push(closed);
      },
      view: {
         checkboxEls: [
            _checkbox(arrivalStatus, true),
         ],
      },
   });

   assert.deepEqual(confirms, []);
   assert.deepEqual(closes, [closed]);
});


test('Test_CreateItinerarySettingsController_TestCloseWithChanges_ExpectConfirm', async () => {
   const persistCalls = [];
   const confirms = [];
   const closes = [];
   const arrivalStatus = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: arrivalStatus,
                  isSuppressable: true,
                  isSuppressed: false,
               },
            ],
         },
      }),
      persistSuppression: async (status) => {
         persistCalls.push({ action: 'suppress', status });
      },
      showConfirmPopup: (args) => {
         confirms.push(args);
      },
      showOverlay: (args) => {
         overlayArgs = args;
      },
   });

   await control.open();
   overlayArgs.onClose({
      close: () => {
         closes.push(true);
      },
      view: {
         checkboxEls: [
            _checkbox(arrivalStatus, false),
         ],
      },
   });

   assert.equal(confirms.length, 1);
   assert.equal(confirms[Position.FIRST].title, Strings.itinerary.confirmation.saveChangesTitle);
   assert.equal(confirms[Position.FIRST].message, Strings.itinerary.settings.saveChangesMessage);
   assert.equal(confirms[Position.FIRST].confirmText, Strings.actions.save);
   assert.equal(confirms[Position.FIRST].cancelText, Strings.itinerary.actions.discard);
   assert.deepEqual(closes, []);
   assert.deepEqual(persistCalls, []);
});


test('Test_CreateItinerarySettingsController_TestConfirmChanges_ExpectPersistAndClose', async () => {
   const persistCalls = [];
   const confirms = [];
   const closes = [];
   const closed = true;
   const suppressAction = 'suppress';
   const arrivalStatus = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: arrivalStatus,
                  isSuppressable: true,
                  isSuppressed: false,
               },
            ],
         },
      }),
      persistSuppression: async (status) => {
         persistCalls.push({ action: suppressAction, status });
      },
      showConfirmPopup: (args) => {
         confirms.push(args);
      },
      showOverlay: (args) => {
         overlayArgs = args;
      },
   });

   await control.open();
   overlayArgs.onClose({
      close: () => {
         closes.push(closed);
      },
      view: {
         checkboxEls: [
            _checkbox(arrivalStatus, false),
         ],
      },
   });
   await confirms[Position.FIRST].onConfirm();

   assert.deepEqual(persistCalls, [
      {
         action: suppressAction,
         status: arrivalStatus,
      },
   ]);
   assert.deepEqual(closes, [closed]);
});


test('Test_CreateItinerarySettingsController_TestDiscard_ExpectClosesWithoutPersist', async () => {
   const persistCalls = [];
   const closes = [];
   const closed = true;
   const arrivalStatus = ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE;
   let overlayArgs;
   let confirmArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: arrivalStatus,
                  isSuppressable: true,
                  isSuppressed: false,
               },
            ],
         },
      }),
      persistSuppression: async (status) => {
         persistCalls.push(status);
      },
      showConfirmPopup: (args) => {
         confirmArgs = args;
      },
      showOverlay: (args) => {
         overlayArgs = args;
      },
   });

   await control.open();
   overlayArgs.onClose({
      close: () => {
         closes.push(closed);
      },
      view: {
         checkboxEls: [
            _checkbox(arrivalStatus, false),
         ],
      },
   });
   confirmArgs.onCancel();

   assert.deepEqual(persistCalls, []);
   assert.deepEqual(closes, [closed]);
});


test('Test_CreateItinerarySettingsController_TestLoadThrows_ExpectEmptyStatuses', async () => {
   const overlays = [];
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => {
         throw new Error('load failed');
      },
      showOverlay: (args) => {
         overlays.push(args);
      },
   });

   await control.open();

   assert.deepEqual(overlays[Position.FIRST].statuses, []);
});
