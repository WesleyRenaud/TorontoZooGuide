import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleDateRangeFieldsBuilder } from '../../../../scripts/consoleOperations/templates/consoleDateRangeFieldsBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateDateRangeFields_TestIds_ExpectTwoFields', () => {
   const startDateId = 'start';
   const endDateId = 'end';

   const fragment = ConsoleDateRangeFieldsBuilder.createDateRangeFields({
      startDateId,
      endDateId,
   });

   const startFieldEl = fragment.children[Position.FIRST];
   const endFieldEl = fragment.children[Position.SECOND];
   assert.equal(fragment.children.length, [startDateId, endDateId].length);
   assert.equal(startFieldEl.children[Position.SECOND].id, startDateId);
   assert.equal(endFieldEl.children[Position.SECOND].id, endDateId);
   assert.equal(endFieldEl.children[Position.FIRST].textContent, Strings.labels.lastDay);
   assert.equal(endFieldEl.children[Position.SECOND].placeholder, Strings.placeholders.lastDay);
});
