import assert from 'node:assert/strict';
import test from 'node:test';

import { AmenityOpenControllerFactory } from '../../../../scripts/consoleOperations/forms/amenityOpenControllerFactory.js';
import { EntityOpenFormController } from '../../../../scripts/consoleOperations/forms/entityOpenFormController.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_CreateAmenityOpenController_TestWiring_ExpectOpenFormWithExplicitlyOpen', () => {
   const original = EntityOpenFormController.createEntityOpenFormController;
   const created = { created: true };
   const loadOptions = async () => [];
   const populateOptions = () => {};
   const submitOpenStatus = async () => ({ success: true });
   const entityEl = {};
   const entityLabel = 'Restroom';
   const optionsLabel = 'Restrooms';
   const restroom = 'Near Cafe';
   let captured;

   EntityOpenFormController.createEntityOpenFormController = (options) => {
      captured = options;
      return created;
   };

   try {
      const controller = AmenityOpenControllerFactory.createAmenityOpenController({
         entityEl,
         loadOptions,
         populateOptions,
         submitOpenStatus,
         entityLabel,
         optionsLabel,
         resultName: result => result.restroom,
      });

      assert.equal(controller, created);
      assert.equal(captured.entityEl, entityEl);
      assert.equal(captured.loadOptions, loadOptions);
      assert.equal(captured.populateOptions, populateOptions);
      assert.equal(captured.submitOpenStatus, submitOpenStatus);
      assert.equal(captured.entityLabel, entityLabel);
      assert.equal(captured.optionsLabel, optionsLabel);
      assert.equal(
         captured.successMessage({ restroom }),
         Strings.status.explicitlyOpen(restroom)
      );
   } finally {
      EntityOpenFormController.createEntityOpenFormController = original;
   }
});


test('Test_CreateAmenityOpenController_TestSuccessMessageOverride_ExpectPassThrough', () => {
   const original = EntityOpenFormController.createEntityOpenFormController;
   const station = 'Main Station';
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

      const message = captured.successMessage({ transportation_station: station });

      assert.equal(message, Strings.status.open(station));
   } finally {
      EntityOpenFormController.createEntityOpenFormController = original;
   }
});
