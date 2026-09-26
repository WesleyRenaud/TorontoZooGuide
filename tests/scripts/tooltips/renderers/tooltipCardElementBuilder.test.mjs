import assert from 'node:assert/strict';
import test from 'node:test';

import { TooltipCardElementBuilder } from '../../../../scripts/tooltips/renderers/tooltipCardElementBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateTooltipCardShell_TestFirstIndex_ExpectVisible', () => {
   const first = TooltipCardElementBuilder.createTooltipCardShell(Position.FIRST);

   assert.equal(first.style.display, 'flex');
   assert.equal(first.dataset.index, String(Position.FIRST));
});


test('Test_CreateTooltipCardShell_TestLaterIndex_ExpectHidden', () => {
   const second = TooltipCardElementBuilder.createTooltipCardShell(Position.SECOND);

   assert.equal(second.style.display, 'none');
});


test('Test_ApplyDataset_TestValues_ExpectWritten', () => {
   const el = document.createElement('div');
   const species = 'African Lion';

   TooltipCardElementBuilder.applyDataset(el, { species, skip: null });

   assert.equal(el.dataset.species, species);
   assert.equal(el.dataset.skip, undefined);
});


test('Test_CreateTooltipImageFrame_TestWithoutFallback_ExpectImage', () => {
   const src = 'lion.jpg';
   const alt = 'African Lion';

   const frame = TooltipCardElementBuilder.createTooltipImageFrame({
      src,
      alt,
   });
   const image = frame.querySelector('img');

   assert.equal(frame.className, 'tooltip-image-frame');
   assert.equal(image.src, src);
   assert.equal(image.alt, alt);
   assert.equal(image.className, 'tooltip-image');
});


test('Test_CreateTooltipImageFrame_TestError_ExpectFallbackSrc', () => {
   const fallbackSrc = 'fallback.jpg';

   const frame = TooltipCardElementBuilder.createTooltipImageFrame({
      src: 'missing.jpg',
      alt: 'African Lion',
      fallbackSrc,
   });
   const image = frame.querySelector('img');
   image.removeEventListener = () => {};
   image.listeners.error?.();

   assert.equal(image.src, fallbackSrc);
});


test('Test_CreateTextElement_TestTagAndDataset_ExpectElement', () => {
   const text = 'Hello';
   const className = 'tooltip-body';
   const species = 'African Lion';

   const element = TooltipCardElementBuilder.createTextElement('p', text, {
      className,
      dataset: { species, skip: null },
   });

   assert.equal(element.tagName, 'p');
   assert.equal(element.textContent, text);
   assert.equal(element.className, className);
   assert.equal(element.dataset.species, species);
   assert.equal(element.dataset.skip, undefined);
});


test('Test_CreateTooltipLinkLine_TestHref_ExpectLink', () => {
   const href = 'https://example.com';
   const text = 'Learn more';
   const className = 'external';

   const line = TooltipCardElementBuilder.createTooltipLinkLine({
      href,
      text,
      className,
   });
   const link = line.querySelector('a');

   assert.equal(link.href, href);
   assert.equal(link.target, '_blank');
   assert.equal(link.rel, 'noopener noreferrer');
   assert.equal(link.textContent, text);
   assert.equal(link.className, `tooltip-link ${className}`);
});


test('Test_CreateTooltipLinkLine_TestDefaultClass_ExpectTooltipLink', () => {
   const href = 'https://example.com';
   const text = 'Learn more';

   const line = TooltipCardElementBuilder.createTooltipLinkLine({
      href,
      text,
   });
   const link = line.querySelector('a');

   assert.equal(link.className, 'tooltip-link');
});
