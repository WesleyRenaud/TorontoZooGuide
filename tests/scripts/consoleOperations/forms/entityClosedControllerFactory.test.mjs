import assert from 'node:assert/strict';
import test from 'node:test';

import { EntityClosedControllerFactory } from '../../../../scripts/consoleOperations/forms/entityClosedControllerFactory.js';
import { EntityClosedFormController } from '../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_CreateEntityClosedController_TestWiring_ExpectClosedFormWithSuccessMessage', async () => {
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

      const controller = EntityClosedControllerFactory.createEntityClosedController({
         entityEl,
         loadOptions,
         populateOptions,
         submitClosedStatus,
         entityLabel: 'Attraction',
         optionsLabel: 'Attractions',
         resultName: result => result.attraction,
      });

      assert.deepEqual(controller, { created: true });
      assert.equal(captured.entityEl, entityEl);
      assert.equal(captured.loadOptions, loadOptions);
      assert.equal(captured.populateOptions, populateOptions);
      assert.equal(captured.submitClosedStatus, submitClosedStatus);
      assert.equal(captured.entityLabel, 'Attraction');
      assert.equal(captured.optionsLabel, 'Attractions');
      assert.equal(
         captured.successMessage({ attraction: 'Carousel' }),
         Strings.status.closed('Carousel')
      );
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
