import assert from 'node:assert/strict';
import test from 'node:test';

import { CarouselView } from '../../../scripts/tooltips/carouselView.js';
import { Strings } from '../../../scripts/strings.js';
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

test('Test_CreateTooltipCarouselView_TestRenderStepJumpClear_ExpectCards', () => {
   const indexChanges = [];
   const tooltipEl = document.createElement('div');
   const view = CarouselView.createTooltipCarouselView({
      tooltipEl,
      getRendererForItem: (item) => (
         item.skip
            ? null
            : _createRenderer()
      ),
      onIndexChange: (index) => { indexChanges.push(index); },
   });

   assert.equal(view.render([]), false);
   assert.ok(tooltipEl.classList.contains('no-arrows'));

   assert.equal(
      view.render([
         { name: 'A' },
         { name: 'Skip', skip: true },
         { name: 'B' },
      ]),
      true
   );
   assert.equal(tooltipEl.querySelector('.tooltip-carousel').children.length, 2);
   assert.equal(tooltipEl.classList.contains('no-arrows'), false);
   assert.equal(
      tooltipEl.querySelector('.tooltip-prev')?.textContent,
      Strings.common.previousSymbol
   );
   assert.equal(
      tooltipEl.querySelector('.tooltip-next')?.textContent,
      Strings.common.nextSymbol
   );

   view.showFirst();
   assert.deepEqual(indexChanges.at(-1), 0);
   view.step(1);
   assert.equal(indexChanges.at(-1), 2);

   tooltipEl.querySelector('.tooltip-prev').click();
   assert.equal(indexChanges.at(-1), 0);

   view.jumpTo((item) => item.name === 'A');
   assert.equal(indexChanges.at(-1), 0);
   view.jumpTo((item) => item.name === 'Missing');
   assert.equal(indexChanges.at(-1), 0);

   view.clear();
   assert.equal(tooltipEl.children.length, 0);
   assert.ok(tooltipEl.classList.contains('no-arrows'));

   view.step(1);
   view.showIndex(1);
   view.jumpTo(() => true);
});

test('Test_CreateTooltipCarouselView_TestSingleCard_ExpectNoArrows', () => {
   const tooltipEl = document.createElement('div');
   const view = CarouselView.createTooltipCarouselView({
      tooltipEl,
      getRendererForItem: () => _createRenderer(),
      onIndexChange: () => {},
   });

   assert.equal(view.render([{ name: 'Only' }]), true);
   assert.ok(tooltipEl.classList.contains('no-arrows'));
   assert.equal(tooltipEl.querySelector('.tooltip-nav'), null);
});

test('Test_CreateTooltipCarouselView_TestNonArrayItems_ExpectCleared', () => {
   const tooltipEl = document.createElement('div');
   const view = CarouselView.createTooltipCarouselView({
      tooltipEl,
      getRendererForItem: () => _createRenderer(),
      onIndexChange: () => {},
   });

   assert.equal(view.render(null), false);
   assert.equal(tooltipEl.children.length, 0);
});
