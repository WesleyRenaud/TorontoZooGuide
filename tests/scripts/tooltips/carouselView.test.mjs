import assert from 'node:assert/strict';
import test from 'node:test';

import { CarouselView } from '../../../scripts/tooltips/carouselView.js';
import { Strings } from '../../../scripts/strings.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../helpers/domTestSetup.mjs';

installDomTestHooks();


function _createRenderer() {
   return {
      createCard(item, index) {
         const card = document.createElement('div');
         card.className = 'tooltip-card';
         card.textContent = `${item.name}:${index}`;
         return card;
      },
   };
}


function _createView(tooltipEl, overrides = {}) {
   return CarouselView.createTooltipCarouselView({
      tooltipEl,
      getRendererForItem: () => _createRenderer(),
      onIndexChange: () => {},
      ...overrides,
   });
}


test('Test_CreateTooltipCarouselView_TestEmpty_ExpectNoArrows', () => {
   const tooltipEl = document.createElement('div');
   const view = _createView(tooltipEl);

   const rendered = view.render([]);

   assert.equal(rendered, false);
   assert.ok(tooltipEl.classList.contains('no-arrows'));
});


test('Test_CreateTooltipCarouselView_TestSkipItem_ExpectRenderableCards', () => {
   const tooltipEl = document.createElement('div');
   const first = { name: 'African Lion' };
   const skipped = { name: 'Skip', skip: true };
   const second = { name: 'Amur Tiger' };

   const view = _createView(tooltipEl, {
      getRendererForItem: (item) => (item.skip ? null : _createRenderer()),
   });
   const rendered = view.render([first, skipped, second]);

   assert.equal(rendered, true);
   assert.equal(tooltipEl.querySelector('.tooltip-carousel').children.length, 2);
   assert.equal(tooltipEl.classList.contains('no-arrows'), false);
   assert.equal(tooltipEl.querySelector('.tooltip-prev')?.textContent, Strings.common.previousSymbol);
   assert.equal(tooltipEl.querySelector('.tooltip-next')?.textContent, Strings.common.nextSymbol);
});


test('Test_CreateTooltipCarouselView_TestStepAndJump_ExpectIndexChanges', () => {
   const indexChanges = [];
   const tooltipEl = document.createElement('div');
   const first = { name: 'African Lion' };
   const skipped = { name: 'Skip', skip: true };
   const second = { name: 'Amur Tiger' };

   const view = _createView(tooltipEl, {
      getRendererForItem: (item) => (item.skip ? null : _createRenderer()),
      onIndexChange: (index) => {
         indexChanges.push(index);
      },
   });
   view.render([first, skipped, second]);
   view.showFirst();
   view.step(1);
   tooltipEl.querySelector('.tooltip-prev').click();
   view.jumpTo((item) => item.name === first.name);
   view.jumpTo((item) => item.name === 'Missing');

   assert.equal(indexChanges.at(Position.LAST), Position.FIRST);
});


test('Test_CreateTooltipCarouselView_TestClear_ExpectEmpty', () => {
   const tooltipEl = document.createElement('div');
   const view = _createView(tooltipEl);
   view.render([{ name: 'African Lion' }, { name: 'Amur Tiger' }]);

   view.clear();
   view.step(1);
   view.showIndex(1);
   view.jumpTo(() => true);

   assert.equal(tooltipEl.children.length, Position.FIRST);
   assert.ok(tooltipEl.classList.contains('no-arrows'));
});


test('Test_CreateTooltipCarouselView_TestEmptyCarouselCards_ExpectShowIndexNoop', () => {
   const indexChanges = [];
   const tooltipEl = document.createElement('div');
   const view = _createView(tooltipEl, {
      onIndexChange: (index) => {
         indexChanges.push(index);
      },
   });
   view.render([{ name: 'African Lion' }]);
   tooltipEl.querySelector('.tooltip-carousel').replaceChildren();

   view.showIndex(Position.FIRST);

   assert.deepEqual(indexChanges, []);
});


test('Test_CreateTooltipCarouselView_TestSingleCard_ExpectNoArrows', () => {
   const tooltipEl = document.createElement('div');
   const view = _createView(tooltipEl);

   const rendered = view.render([{ name: 'African Lion' }]);

   assert.equal(rendered, true);
   assert.ok(tooltipEl.classList.contains('no-arrows'));
   assert.equal(tooltipEl.querySelector('.tooltip-nav'), null);
});


test('Test_CreateTooltipCarouselView_TestNonArrayItems_ExpectCleared', () => {
   const tooltipEl = document.createElement('div');
   const view = _createView(tooltipEl);

   const rendered = view.render(null);

   assert.equal(rendered, false);
   assert.equal(tooltipEl.children.length, Position.FIRST);
});


test('Test_CreateTooltipCarouselView_TestOnClose_ExpectCloseButton', () => {
   const tooltipEl = document.createElement('div');
   let closes = 0;
   const view = _createView(tooltipEl, { onClose: () => { closes += 1; } });

   view.render([{ name: 'African Lion' }]);
   const closeButton = tooltipEl.querySelector('.tooltip-close');
   closeButton.click();

   assert.equal(String(closeButton.tagName).toLowerCase(), 'button');
   assert.equal(closeButton.type, 'button');
   assert.equal(closeButton.textContent, Strings.common.closeSymbol);
   assert.equal(closeButton.getAttribute('aria-label'), Strings.tooltips.closeDetailsAria);
   assert.equal(closes, 1);
});


test('Test_CreateTooltipCarouselView_TestWithoutOnClose_ExpectNoCloseButton', () => {
   const tooltipEl = document.createElement('div');
   const view = _createView(tooltipEl);

   view.render([{ name: 'African Lion' }]);

   assert.equal(tooltipEl.querySelector('.tooltip-close'), null);
});


test('Test_CreateTooltipCarouselView_TestArrows_ExpectKeyboardOperableButtons', () => {
   const tooltipEl = document.createElement('div');
   const indices = [];
   const view = _createView(tooltipEl, { onIndexChange: (index) => indices.push(index) });

   view.render([{ name: 'African Lion' }, { name: 'Amur Tiger' }]);
   view.showFirst();
   const prev = tooltipEl.querySelector('.tooltip-prev');
   const next = tooltipEl.querySelector('.tooltip-next');
   const enterNotPrevented = next.dispatchEvent({ type: 'keydown', key: 'Enter' });
   next.dispatchEvent({ type: 'keydown', key: ' ' });
   const otherNotPrevented = prev.dispatchEvent({ type: 'keydown', key: 'a' });

   assert.equal(prev.getAttribute('role'), 'button');
   assert.equal(prev.getAttribute('tabindex'), '0');
   assert.equal(prev.getAttribute('aria-label'), Strings.tooltips.previousCardAria);
   assert.equal(next.getAttribute('aria-label'), Strings.tooltips.nextCardAria);
   assert.equal(enterNotPrevented, false);
   assert.equal(otherNotPrevented, true);
   assert.deepEqual(indices, [0, 1, 0]);
});
