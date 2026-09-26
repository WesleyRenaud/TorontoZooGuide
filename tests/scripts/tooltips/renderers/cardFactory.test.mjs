import assert from 'node:assert/strict';
import test from 'node:test';

import { Position } from '../../../../scripts/shared/enums/position.js';
import { CardFactory } from '../../../../scripts/tooltips/renderers/cardFactory.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateTooltipCard_TestTitleAndDetails_ExpectCard', () => {
   const title = 'Zootique';
   const detail = 'Gift shop';

   const card = CardFactory.createTooltipCard({
      index: Position.FIRST,
      title: { text: title },
      details: [detail, ''],
   });

   assert.equal(card.className, 'tooltip-card');
   assert.match(card.textContent, new RegExp(title));
   assert.match(card.textContent, new RegExp(detail));
});
