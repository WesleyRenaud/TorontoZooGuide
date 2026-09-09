import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityOpenControllerFactory } from '../../../../scripts/consoleOperations/forms/amenityOpenControllerFactory.js';
import { EntityOpenFormController } from '../../../../scripts/consoleOperations/forms/entityOpenFormController.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_CreateAmenityOpenController_TestWiring_ExpectOpenFormWithExplicitlyOpen', async () => {
   const original = EntityOpenFormController.createEntityOpenFormController;
   let captured;

   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      const loadOptions = async () => [];
      const populateOptions = () => {};
      const submitOpenStatus = async () => ({ success: true });
      const entityEl = {};

      const controller = AmenityOpenControllerFactory.createAmenityOpenController({
         entityEl,
         loadOptions,
         populateOptions,
         submitOpenStatus,
         entityLabel: 'Restroom',
         optionsLabel: 'Restrooms',
         resultName: result => result.restroom,
      });

      assert.deepEqual(controller, { created: true });
      assert.equal(captured.entityEl, entityEl);
      assert.equal(captured.loadOptions, loadOptions);
      assert.equal(captured.populateOptions, populateOptions);
      assert.equal(captured.submitOpenStatus, submitOpenStatus);
      assert.equal(captured.entityLabel, 'Restroom');
      assert.equal(captured.optionsLabel, 'Restrooms');
      assert.equal(
         captured.successMessage({ restroom: 'Near Cafe' }),
         Strings.status.explicitlyOpen('Near Cafe')
      );
   } finally {
      EntityOpenFormController.createEntityOpenFormController = original;
   }
});

test('Test_CreateAmenityOpenController_TestSuccessMessageOverride_ExpectPassThrough', async () => {
   const original = EntityOpenFormController.createEntityOpenFormController;
   let captured;

   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return { created: true };
   };

   try {
      AmenityOpenControllerFactory.createAmenityOpenController({
         entityEl: {},
         loadOptions: async () => [],
         populateOptions: () => {},
         submitOpenStatus: async () => ({ success: true }),
         entityLabel: 'Station',
         optionsLabel: 'Stations',
         successMessage: result => Strings.status.open(result.transportation_station),
      });

      assert.equal(
         captured.successMessage({ transportation_station: 'Main Station' }),
         Strings.status.open('Main Station')
      );
   } finally {
      EntityOpenFormController.createEntityOpenFormController = original;
   }
});
