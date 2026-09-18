import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySettingsController } from '../../../../scripts/itinerary/settings/itinerarySettingsController.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _checkbox(status, checked) {
   return {
      checked,
      dataset: { status },
   };
}

test('Test_CreateItinerarySettingsController_TestGearClick_ExpectSuppressableStatuses', async () => {
   const overlays = [];
   const gearEl = document.createElement('button');
   const mountEl = document.getElementById('itineraryFlow');

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
               {
                  status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
                  isSuppressable: true,
                  isSuppressed: true,
               },
               {
                  status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
                  isSuppressable: true,
                  isSuppressed: false,
               },
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
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ]
   );
});

test('Test_CreateItinerarySettingsController_TestSave_ExpectPersistAndClose', async () => {
   const persistCalls = [];
   const closes = [];
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      gearEl: document.createElement('button'),
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
                  isSuppressable: true,
                  isSuppressed: false,
               },
               {
                  status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
                  isSuppressable: true,
                  isSuppressed: true,
               },
            ],
         },
      }),
      persistSuppression: async (status) => {
         persistCalls.push({ action: 'suppress', status });
      },
      persistUnsuppression: async (status) => {
         persistCalls.push({ action: 'unsuppress', status });
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
            _checkbox(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE, false),
            _checkbox(ItineraryErrorType.ITEM_NOT_ON_ITINERARY, true),
         ],
      },
   });

   assert.deepEqual(persistCalls, [
      {
         action: 'suppress',
         status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
      },
      {
         action: 'unsuppress',
         status: ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      },
   ]);
   assert.deepEqual(closes, [true]);
});

test('Test_CreateItinerarySettingsController_TestSaveUnchanged_ExpectClosesWithoutPersist', async () => {
   const persistCalls = [];
   const closes = [];
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
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
         closes.push(true);
      },
      view: {
         checkboxEls: [
            _checkbox(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE, true),
         ],
      },
   });

   assert.deepEqual(persistCalls, []);
   assert.deepEqual(closes, [true]);
});

test('Test_CreateItinerarySettingsController_TestSaveThrows_ExpectStaysOpen', async () => {
   const closes = [];
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
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
            _checkbox(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE, false),
         ],
      },
   });

   assert.deepEqual(closes, []);
});

test('Test_CreateItinerarySettingsController_TestCloseWithoutChanges_ExpectCloses', async () => {
   const confirms = [];
   const closes = [];
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
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
         closes.push(true);
      },
      view: {
         checkboxEls: [
            _checkbox(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE, true),
         ],
      },
   });

   assert.deepEqual(confirms, []);
   assert.deepEqual(closes, [true]);
});

test('Test_CreateItinerarySettingsController_TestCloseWithChanges_ExpectConfirm', async () => {
   const persistCalls = [];
   const confirms = [];
   const closes = [];
   let overlayArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
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
            _checkbox(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE, false),
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

   await confirms[Position.FIRST].onConfirm();
   assert.deepEqual(persistCalls, [
      {
         action: 'suppress',
         status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
      },
   ]);
   assert.deepEqual(closes, [true]);
});

test('Test_CreateItinerarySettingsController_TestDiscard_ExpectClosesWithoutPersist', async () => {
   const persistCalls = [];
   const closes = [];
   let overlayArgs;
   let confirmArgs;
   const control = ItinerarySettingsController.createItinerarySettingsController({
      loadItinerary: async () => ({
         itineraryConfig: {
            statuses: [
               {
                  status: ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
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
         closes.push(true);
      },
      view: {
         checkboxEls: [
            _checkbox(ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE, false),
         ],
      },
   });

   confirmArgs.onCancel();
   assert.deepEqual(persistCalls, []);
   assert.deepEqual(closes, [true]);
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
