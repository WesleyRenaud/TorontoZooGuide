import assert from 'node:assert/strict';
import test from 'node:test';

import { FocusFromQueryHelper } from '../../../scripts/focus/focusFromQueryHelper.js';

test('Test_GetFocusRequestFromQuery_TestParams_ExpectRequestOrNull', () => {
   assert.deepEqual(
      FocusFromQueryHelper.getFocusRequestFromQuery('?focus=African%20Lion&exhibit=African%20Savanna'),
      { species: 'African Lion', exhibit: 'African Savanna' }
   );
   assert.deepEqual(
      FocusFromQueryHelper.getFocusRequestFromQuery('?focus=African%20Lion'),
      { species: 'African Lion', exhibit: null }
   );
   assert.equal(FocusFromQueryHelper.getFocusRequestFromQuery('?other=1'), null);
});
