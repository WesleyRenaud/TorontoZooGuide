import assert from 'node:assert/strict';
import test from 'node:test';

import { ValidationBubbleHelper } from '../../scripts/validationBubbleHelper.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ResolveClassNames_TestOverrides_ExpectMerged', () => {
   const bubble = 'custom-bubble';

   const classNames = ValidationBubbleHelper.resolveClassNames({
      bubble,
   });

   assert.deepEqual(classNames, {
      ...ValidationBubbleHelper.DEFAULT_CLASS_NAMES,
      bubble,
   });
});


test('Test_PositionValidationBubble_TestBelowAnchor_ExpectStyles', () => {
   const bubbleWidth = 100;
   const bubbleHeight = 40;
   const anchorLeft = 30;
   const anchorTop = 10;
   const anchorWidth = 40;
   const anchorHeight = 20;
   const bubbleEl = document.createElement('div');
   const anchorEl = document.createElement('button');
   const properties = {};
   bubbleEl.getBoundingClientRect = () => ({
      width: bubbleWidth,
      height: bubbleHeight,
      top: 0,
      left: 0,
      right: bubbleWidth,
      bottom: bubbleHeight,
   });
   anchorEl.getBoundingClientRect = () => ({
      width: anchorWidth,
      height: anchorHeight,
      top: anchorTop,
      left: anchorLeft,
      right: anchorLeft + anchorWidth,
      bottom: anchorTop + anchorHeight,
   });
   bubbleEl.style.setProperty = (name, value) => {
      properties[name] = value;
   };
   globalThis.window.innerWidth = 400;
   globalThis.window.innerHeight = 400;

   ValidationBubbleHelper.positionValidationBubble(bubbleEl, anchorEl);

   assert.equal(bubbleEl.style.left, `${anchorLeft}px`);
   assert.equal(
      bubbleEl.style.top,
      `${anchorTop + anchorHeight + ValidationBubbleHelper.ANCHOR_GAP}px`
   );
   assert.equal(
      properties['--tzg-validation-bubble-arrow-left'],
      `${anchorWidth / 2}px`
   );
});


test('Test_PositionValidationBubble_TestNearEdges_ExpectClamped', () => {
   const bubbleWidth = 120;
   const bubbleHeight = 50;
   const viewportSize = 400;
   const anchorLeft = 350;
   const anchorTop = 360;
   const anchorSize = 20;
   const bubbleEl = document.createElement('div');
   const anchorEl = document.createElement('button');
   const properties = {};
   bubbleEl.getBoundingClientRect = () => ({
      width: bubbleWidth,
      height: bubbleHeight,
      top: 0,
      left: 0,
      right: bubbleWidth,
      bottom: bubbleHeight,
   });
   anchorEl.getBoundingClientRect = () => ({
      width: anchorSize,
      height: anchorSize,
      top: anchorTop,
      left: anchorLeft,
      right: anchorLeft + anchorSize,
      bottom: anchorTop + anchorSize,
   });
   bubbleEl.style.setProperty = (name, value) => {
      properties[name] = value;
   };
   globalThis.window.innerWidth = viewportSize;
   globalThis.window.innerHeight = viewportSize;

   ValidationBubbleHelper.positionValidationBubble(bubbleEl, anchorEl);

   assert.equal(
      bubbleEl.style.left,
      `${viewportSize - bubbleWidth - ValidationBubbleHelper.VIEWPORT_PADDING}px`
   );
   assert.ok(Number.parseInt(bubbleEl.style.top, 10) < anchorTop);
   assert.ok(properties['--tzg-validation-bubble-arrow-left']);
});
