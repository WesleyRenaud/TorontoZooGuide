import assert from 'node:assert/strict';
import test from 'node:test';

import { TooltipCardElementBuilder } from '../../../../scripts/tooltips/renderers/tooltipCardElementBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateTooltipCardShell_TestIndex_ExpectVisibility', () => {
   const first = TooltipCardElementBuilder.createTooltipCardShell(0);
   const second = TooltipCardElementBuilder.createTooltipCardShell(1);
   assert.equal(first.style.display, 'flex');
   assert.equal(second.style.display, 'none');
   assert.equal(first.dataset.index, '0');
});

test('Test_ApplyDataset_TestValues_ExpectWritten', () => {
   const el = document.createElement('div');
   TooltipCardElementBuilder.applyDataset(el, { species: 'Lion', skip: null });
   assert.equal(el.dataset.species, 'Lion');
   assert.equal(el.dataset.skip, undefined);
});

test('Test_CreateTooltipImageFrame_TestWithoutFallback_ExpectImage', () => {
   const frame = TooltipCardElementBuilder.createTooltipImageFrame({
      src: 'lion.jpg',
      alt: 'Lion',
   });

   const image = frame.querySelector('img');
   assert.equal(frame.className, 'tooltip-image-frame');
   assert.equal(image.src, 'lion.jpg');
   assert.equal(image.alt, 'Lion');
   assert.equal(image.className, 'tooltip-image');
});

test('Test_CreateTooltipImageFrame_TestError_ExpectFallbackSrc', () => {
   const frame = TooltipCardElementBuilder.createTooltipImageFrame({
      src: 'missing.jpg',
      alt: 'Lion',
      fallbackSrc: 'fallback.jpg',
   });
   const image = frame.querySelector('img');
   image.removeEventListener = () => {};

   image.listeners.error?.();

   assert.equal(image.src, 'fallback.jpg');
});

test('Test_CreateTextElement_TestTagAndDataset_ExpectElement', () => {
   const element = TooltipCardElementBuilder.createTextElement('p', 'Hello', {
      className: 'tooltip-body',
      dataset: { species: 'Lion', skip: null },
   });

   assert.equal(element.tagName, 'p');
   assert.equal(element.textContent, 'Hello');
   assert.equal(element.className, 'tooltip-body');
   assert.equal(element.dataset.species, 'Lion');
   assert.equal(element.dataset.skip, undefined);
});

test('Test_CreateTooltipLinkLine_TestHref_ExpectLink', () => {
   const line = TooltipCardElementBuilder.createTooltipLinkLine({
      href: 'https://example.com',
      text: 'Learn more',
      className: 'external',
   });
   const link = line.querySelector('a');

   assert.equal(link.href, 'https://example.com');
   assert.equal(link.target, '_blank');
   assert.equal(link.rel, 'noopener noreferrer');
   assert.equal(link.textContent, 'Learn more');
   assert.equal(link.className, 'tooltip-link external');
});

test('Test_CreateTooltipLinkLine_TestDefaultClass_ExpectTooltipLink', () => {
   const line = TooltipCardElementBuilder.createTooltipLinkLine({
      href: 'https://example.com',
      text: 'Learn more',
   });
   const link = line.querySelector('a');

   assert.equal(link.className, 'tooltip-link');
});
