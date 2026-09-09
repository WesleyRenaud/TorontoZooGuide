import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateDateRangeFields_TestIds_ExpectTwoFields', () => {
   const fragment = ConsoleDateRangeFieldsBuilder.createDateRangeFields({
      startDateId: 'start',
      endDateId: 'end',
   });
   assert.equal(fragment.children.length, 2);
   assert.equal(fragment.children[0].children[1].id, 'start');
   assert.equal(fragment.children[1].children[1].id, 'end');
   assert.equal(fragment.children[1].children[0].textContent, Strings.labels.lastDay);
   assert.equal(fragment.children[1].children[1].placeholder, Strings.placeholders.lastDay);
});
