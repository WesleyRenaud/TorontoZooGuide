import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityClosureControllerFactory } from '../../../../scripts/consoleOperations/forms/amenityClosureControllerFactory.js';
import { EntityClosedFormController } from '../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_CreateAmenityClosureController_TestWiring_ExpectClosedFormWithSuccessMessage', () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   const created = { created: true };
   const loadOptions = async () => [];
   const populateOptions = () => {};
   const submitClosedStatus = async () => ({ success: true });
   const entityEl = {};
   const entityLabel = 'Gift Shop';
   const optionsLabel = 'Gift Shops';
   const giftShop = 'Zootique';
   let captured;

   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return created;
   };

   try {
      const controller = AmenityClosureControllerFactory.createAmenityClosureController({
         entityEl,
         loadOptions,
         populateOptions,
         submitClosedStatus,
         entityLabel,
         optionsLabel,
         resultName: result => result.gift_shop,
      });

      assert.equal(controller, created);
      assert.equal(captured.entityEl, entityEl);
      assert.equal(captured.loadOptions, loadOptions);
      assert.equal(captured.populateOptions, populateOptions);
      assert.equal(captured.submitClosedStatus, submitClosedStatus);
      assert.equal(captured.entityLabel, entityLabel);
      assert.equal(captured.optionsLabel, optionsLabel);
      assert.equal(
         captured.successMessage({ gift_shop: giftShop }),
         Strings.status.closureOverrideSaved(giftShop)
      );
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
