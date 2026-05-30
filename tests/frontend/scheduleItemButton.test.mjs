import assert from 'node:assert/strict';
import { afterEach, test } from 'node:test';

import { makeScheduleItemButton } from '../../scripts/itinerary/panel/components/scheduleItemButton.js';
import {
   installDocument,
   teardownDocument,
} from './helpers/domMock.mjs';

afterEach(() => {
   teardownDocument();
});

test('makeScheduleItemButton wires an optional click handler', () => {
   installDocument();

   let clicked = false;
   const row = makeScheduleItemButton({
      label: 'Schedule an item',
      onClick: () => {
         clicked = true;
      },
   });
   const button = row.children[0];

   assert.equal(button.textContent, 'Schedule an item');
   assert.equal(button.type, 'button');

   button.listeners.click();
   assert.equal(clicked, true);
});
