import assert from 'node:assert/strict';
import test from 'node:test';

import { APP_STRINGS } from '../../scripts/strings.js';

test('schedule override selection confirmation copy is defined', () => {
   assert.equal(
      APP_STRINGS.itinerary.confirmation.scheduleOverrideSelectionTitle,
      'Adjust Activity Times?'
   );
   assert.match(
      APP_STRINGS.itinerary.confirmation.scheduleOverrideSelectionMessage,
      /overlap in time/
   );
   assert.match(
      APP_STRINGS.itinerary.confirmation.scheduleOverrideSelectionMessage,
      /Wild Encounters taking priority/
   );
});
