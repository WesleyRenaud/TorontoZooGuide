import assert from 'node:assert/strict';
import test from 'node:test';

import { ValidationBubbleHelper } from '../../scripts/validationBubbleHelper.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ResolveClassNames_TestOverrides_ExpectMerged', () => {
   assert.deepEqual(ValidationBubbleHelper.resolveClassNames({
      bubble: 'custom-bubble',
   }), {
      ...ValidationBubbleHelper.DEFAULT_CLASS_NAMES,
      bubble: 'custom-bubble',
   });
});

test('Test_PositionValidationBubble_TestBelowAnchor_ExpectStyles', () => {
   const bubbleEl = document.createElement('div');
   const anchorEl = document.createElement('button');
   const properties = {};

   bubbleEl.getBoundingClientRect = () => ({
      width: 100,
      height: 40,
      top: 0,
      left: 0,
      right: 100,
      bottom: 40,
   });
   anchorEl.getBoundingClientRect = () => ({
      width: 40,
      height: 20,
      top: 10,
      left: 30,
      right: 70,
      bottom: 30,
   });
   bubbleEl.style.setProperty = (name, value) => {
      properties[name] = value;
   };

   globalThis.window.innerWidth = 400;
   globalThis.window.innerHeight = 400;

   ValidationBubbleHelper.positionValidationBubble(bubbleEl, anchorEl);

   assert.equal(bubbleEl.style.left, '30px');
   assert.equal(bubbleEl.style.top, '42px');
   assert.equal(properties['--tzg-validation-bubble-arrow-left'], '20px');
});

test('Test_PositionValidationBubble_TestNearEdges_ExpectClamped', () => {
   const bubbleEl = document.createElement('div');
   const anchorEl = document.createElement('button');
   const properties = {};

   bubbleEl.getBoundingClientRect = () => ({
      width: 120,
      height: 50,
      top: 0,
      left: 0,
      right: 120,
      bottom: 50,
   });
   anchorEl.getBoundingClientRect = () => ({
      width: 20,
      height: 20,
      top: 360,
      left: 350,
      right: 370,
      bottom: 380,
   });
   bubbleEl.style.setProperty = (name, value) => {
      properties[name] = value;
   };

   globalThis.window.innerWidth = 400;
   globalThis.window.innerHeight = 400;

   ValidationBubbleHelper.positionValidationBubble(bubbleEl, anchorEl);

   assert.equal(bubbleEl.style.left, '268px');
   assert.ok(Number.parseInt(bubbleEl.style.top, 10) < 360);
   assert.ok(properties['--tzg-validation-bubble-arrow-left']);
});
