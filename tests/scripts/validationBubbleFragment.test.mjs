import assert from 'node:assert/strict';
import test from 'node:test';

import { ValidationBubbleFragment } from '../../scripts/validationBubbleFragment.js';
import { ValidationBubbleHelper } from '../../scripts/validationBubbleHelper.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateValidationBubbleController_TestShowAndDismiss_ExpectBubble', () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   const positions = [];
   ValidationBubbleHelper.positionValidationBubble = (...args) => { positions.push(args); };

   const anchorEl = document.createElement('button');
   const controller = ValidationBubbleFragment.createValidationBubbleController({
      anchorEl,
      iconText: '!',
   });

   try {
      controller.show('');
      assert.equal(positions.length, 0);

      controller.show('Required');
      assert.equal(positions.length, 1);
      const bubble = positions[0][0];
      assert.equal(bubble.getAttribute('role'), 'alert');
      assert.match(bubble.textContent, /Required/);

      controller.dismiss();
      controller.show('Again');
      assert.equal(positions.length, 2);
      assert.match(positions[1][0].textContent, /Again/);
   } finally {
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
   }
});
