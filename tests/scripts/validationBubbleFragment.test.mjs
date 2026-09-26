import assert from 'node:assert/strict';
import test from 'node:test';

import { ValidationBubbleFragment } from '../../scripts/validationBubbleFragment.js';
import { ValidationBubbleHelper } from '../../scripts/validationBubbleHelper.js';
import { Position } from '../../scripts/shared/enums/position.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateValidationBubbleController_TestBlankMessage_ExpectNoBubble', () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   const positions = [];
   ValidationBubbleHelper.positionValidationBubble = (...args) => {
      positions.push(args);
   };

   try {
      const controller = ValidationBubbleFragment.createValidationBubbleController({
         anchorEl: document.createElement('button'),
         iconText: '!',
         dismissMs: 0,
      });

      controller.show('');

      assert.equal(positions.length, Position.FIRST);
   } finally {
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
   }
});


test('Test_CreateValidationBubbleController_TestShow_ExpectAlert', () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   const positions = [];
   const message = 'Required';
   ValidationBubbleHelper.positionValidationBubble = (...args) => {
      positions.push(args);
   };

   try {
      const controller = ValidationBubbleFragment.createValidationBubbleController({
         anchorEl: document.createElement('button'),
         iconText: '!',
         dismissMs: 0,
      });

      controller.show(message);
      const bubble = positions.at(Position.FIRST).at(Position.FIRST);

      assert.equal(positions.length, Position.SECOND);
      assert.equal(bubble.getAttribute('role'), 'alert');
      assert.match(bubble.textContent, new RegExp(message));
   } finally {
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
   }
});


test('Test_CreateValidationBubbleController_TestScrollResize_ExpectRepositioned', () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   const originalAdd = window.addEventListener;
   const originalRemove = window.removeEventListener;
   const positions = [];
   const windowListeners = {};
   window.addEventListener = (type, handler) => {
      windowListeners[type] = handler;
   };
   window.removeEventListener = (type) => {
      delete windowListeners[type];
   };
   ValidationBubbleHelper.positionValidationBubble = (...args) => {
      positions.push(args);
   };

   try {
      const controller = ValidationBubbleFragment.createValidationBubbleController({
         anchorEl: document.createElement('button'),
         iconText: '!',
         dismissMs: 0,
      });
      controller.show('Required');
      windowListeners.scroll?.();
      windowListeners.resize?.();

      assert.ok(positions.length >= 3);
   } finally {
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
      window.addEventListener = originalAdd;
      window.removeEventListener = originalRemove;
   }
});


test('Test_CreateValidationBubbleController_TestDismissThenShow_ExpectAgain', () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   const originalAdd = window.addEventListener;
   const originalRemove = window.removeEventListener;
   const positions = [];
   const again = 'Again';
   window.addEventListener = () => {};
   window.removeEventListener = () => {};
   ValidationBubbleHelper.positionValidationBubble = (...args) => {
      positions.push(args);
   };

   try {
      const controller = ValidationBubbleFragment.createValidationBubbleController({
         anchorEl: document.createElement('button'),
         iconText: '!',
         dismissMs: 0,
      });
      controller.show('Required');
      controller.dismiss();
      controller.show(again);

      assert.equal(positions.at(Position.LAST).at(Position.FIRST).textContent.includes(again), true);
   } finally {
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
      window.addEventListener = originalAdd;
      window.removeEventListener = originalRemove;
   }
});


test('Test_CreateValidationBubbleController_TestDismissWithoutRemove_ExpectParentFallback', () => {
   const originalPosition = ValidationBubbleHelper.positionValidationBubble;
   ValidationBubbleHelper.positionValidationBubble = () => {};
   const removed = [];
   const parent = {
      removeChild(child) {
         removed.push(child);
      },
   };
   const originalCreate = document.createElement;
   document.createElement = (tagName) => {
      const node = originalCreate(tagName);
      if (String(tagName).toLowerCase() === 'div') {
         node.remove = undefined;
         Object.defineProperty(node, 'parentElement', {
            configurable: true,
            get: () => parent,
         });
      }
      return node;
   };

   try {
      const controller = ValidationBubbleFragment.createValidationBubbleController({
         anchorEl: document.createElement('button'),
         dismissMs: 0,
      });
      controller.show('Required');
      controller.dismiss();

      assert.equal(removed.length, Position.SECOND);
   } finally {
      document.createElement = originalCreate;
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
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
      const shownCount = document.querySelectorAll('.tzg-validation-bubble').length;
      await new Promise((resolve) => {
         setTimeout(resolve, 20);
      });
      const remainingCount = document.querySelectorAll('.tzg-validation-bubble').length;

      assert.equal(shownCount, Position.SECOND);
      assert.equal(remainingCount, Position.FIRST);
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
   const first = 'First';
   const second = 'Second';
   const anchorEl = document.createElement('button');
   body.appendChild(anchorEl);
   const controller = ValidationBubbleFragment.createValidationBubbleController({
      anchorEl,
      dismissMs: 30,
   });

   try {
      controller.show(first);
      await new Promise((resolve) => {
         setTimeout(resolve, 10);
      });
      controller.show(second);
      const midText = document.querySelector('.tzg-validation-bubble-text')?.textContent;
      await new Promise((resolve) => {
         setTimeout(resolve, 20);
      });
      const stillSecond = document.querySelector('.tzg-validation-bubble-text')?.textContent;
      await new Promise((resolve) => {
         setTimeout(resolve, 20);
      });
      const remainingCount = document.querySelectorAll('.tzg-validation-bubble').length;

      assert.equal(midText, second);
      assert.equal(stillSecond, second);
      assert.equal(remainingCount, Position.FIRST);
   } finally {
      controller.dismiss();
      ValidationBubbleHelper.positionValidationBubble = originalPosition;
   }
});
