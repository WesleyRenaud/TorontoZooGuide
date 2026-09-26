import assert from 'node:assert/strict';
import test from 'node:test';

import { EntityClosedControllerFactory } from '../../../../scripts/consoleOperations/forms/entityClosedControllerFactory.js';
import { EntityClosedFormController } from '../../../../scripts/consoleOperations/forms/entityClosedFormController.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_CreateEntityClosedController_TestWiring_ExpectClosedFormWithSuccessMessage', () => {
   const original = EntityClosedFormController.createEntityClosedFormController;
   const created = { created: true };
   const loadOptions = async () => [];
   const populateOptions = () => {};
   const submitClosedStatus = async () => ({ success: true });
   const entityEl = {};
   const entityLabel = 'Attraction';
   const optionsLabel = 'Attractions';
   const attraction = 'Carousel';
   let captured;

   EntityClosedFormController.createEntityClosedFormController = (options) => {
      captured = options;
      return created;
   };

   try {
      const controller = EntityClosedControllerFactory.createEntityClosedController({
         entityEl,
         loadOptions,
         populateOptions,
         submitClosedStatus,
         entityLabel,
         optionsLabel,
         resultName: result => result.attraction,
      });

      assert.equal(controller, created);
      assert.equal(captured.entityEl, entityEl);
      assert.equal(captured.loadOptions, loadOptions);
      assert.equal(captured.populateOptions, populateOptions);
      assert.equal(captured.submitClosedStatus, submitClosedStatus);
      assert.equal(captured.entityLabel, entityLabel);
      assert.equal(captured.optionsLabel, optionsLabel);
      assert.equal(
         captured.successMessage({ attraction }),
         Strings.status.closed(attraction)
      );
   } finally {
      EntityClosedFormController.createEntityClosedFormController = original;
   }
});
