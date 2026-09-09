import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityClosureControllerFactory } from '../../../../scripts/consoleOperations/forms/amenityClosureControllerFactory.js';
import { EntityClosedFormController } from '../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_CreateAmenityClosureController_TestWiring_ExpectClosedFormWithSuccessMessage', async () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   let captured;

   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      const loadOptions = async () => [];
      const populateOptions = () => {};
      const submitClosedStatus = async () => ({ success: true });
      const entityEl = {};

      const controller = AmenityClosureControllerFactory.createAmenityClosureController({
         entityEl,
         loadOptions,
         populateOptions,
         submitClosedStatus,
         entityLabel: 'Gift Shop',
         optionsLabel: 'Gift Shops',
         resultName: result => result.gift_shop,
      });

      assert.deepEqual(controller, { created: true });
      assert.equal(captured.entityEl, entityEl);
      assert.equal(captured.loadOptions, loadOptions);
      assert.equal(captured.populateOptions, populateOptions);
      assert.equal(captured.submitClosedStatus, submitClosedStatus);
      assert.equal(captured.entityLabel, 'Gift Shop');
      assert.equal(captured.optionsLabel, 'Gift Shops');
      assert.equal(
         captured.successMessage({ gift_shop: 'Zootique' }),
         Strings.status.closureOverrideSaved('Zootique')
      );
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
