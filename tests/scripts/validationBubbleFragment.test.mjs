import assert from 'node:assert/strict';
import test from 'node:test';

import { ValidationBubbleFragment } from '../../scripts/validationBubbleFragment.js';
import { ValidationBubbleHelper } from '../../scripts/validationBubbleHelper.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateValidationBubbleController_TestShowAndDismiss_ExpectBubble', () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   const positions = [];
   const windowListeners = {};
   const originalAdd = window.addEventListener;
   const originalRemove = window.removeEventListener;
   window.addEventListener = (type, handler) => {
      windowListeners[type] = handler;
   };
   window.removeEventListener = (type) => {
      delete windowListeners[type];
   };
   ValidationBubbleHelper.positionValidationBubble = (...args) => { positions.push(args); };

   const anchorEl = document.createElement('button');
   const controller = ValidationBubbleFragment.createValidationBubbleController({
      anchorEl,
      iconText: '!',
      dismissMs: 0,
   });

   try {
      controller.show('');
      assert.equal(positions.length, 0);

      controller.show('Required');
      assert.equal(positions.length, 1);
      const bubble = positions[0][0];
      assert.equal(bubble.getAttribute('role'), 'alert');
      assert.match(bubble.textContent, /Required/);

      windowListeners.scroll?.();
      windowListeners.resize?.();
      assert.ok(positions.length >= 3);

      controller.dismiss();
      controller.show('Again');
      assert.equal(positions.at(-1)[0].textContent.includes('Again'), true);
   } finally {
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
      window.addEventListener = originalAdd;
      window.removeEventListener = originalRemove;
   }
});

test('Test_CreateValidationBubbleController_TestAutoDismiss_ExpectRemoved', async () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   ValidationBubbleHelper.positionValidationBubble = () => {};

   const body = document.body;
   body.appendChild = (child) => {
      child.parentElement = body;
      child.parent = body;
      body.children.push(child);
      return child;
   };

   const anchorEl = document.createElement('button');
   body.appendChild(anchorEl);
   const controller = ValidationBubbleFragment.createValidationBubbleController({
      anchorEl,
      dismissMs: 5,
   });

   try {
      controller.show('Departure time must be after arrival.');
      assert.equal(document.querySelectorAll('.tzg-validation-bubble').length, 1);

      await new Promise((resolve) => {
         setTimeout(resolve, 20);
      });

      assert.equal(document.querySelectorAll('.tzg-validation-bubble').length, 0);
   } finally {
      controller.dismiss();
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
   }
});

test('Test_CreateValidationBubbleController_TestReshowClearsTimer_ExpectOk', async () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   ValidationBubbleHelper.positionValidationBubble = () => {};

   const body = document.body;
   body.appendChild = (child) => {
      child.parentElement = body;
      child.parent = body;
      body.children.push(child);
      return child;
   };

   const anchorEl = document.createElement('button');
   body.appendChild(anchorEl);
   const controller = ValidationBubbleFragment.createValidationBubbleController({
      anchorEl,
      dismissMs: 30,
   });

   try {
      controller.show('First');
      await new Promise((resolve) => {
         setTimeout(resolve, 10);
      });
      controller.show('Second');
      assert.equal(
         document.querySelector('.tzg-validation-bubble-text')?.textContent,
         'Second'
      );

      await new Promise((resolve) => {
         setTimeout(resolve, 20);
      });
      assert.equal(
         document.querySelector('.tzg-validation-bubble-text')?.textContent,
         'Second'
      );

      await new Promise((resolve) => {
         setTimeout(resolve, 20);
      });
      assert.equal(document.querySelectorAll('.tzg-validation-bubble').length, 0);
   } finally {
      controller.dismiss();
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
   }
});
