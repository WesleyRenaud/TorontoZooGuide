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
