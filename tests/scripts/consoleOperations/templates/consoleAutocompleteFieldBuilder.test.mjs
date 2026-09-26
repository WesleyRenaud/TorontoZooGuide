import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleAutocompleteFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleAutocompleteFieldBuilder.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_CreateAutocompleteField_TestConfig_ExpectInputAndResults', () => {
   const inputId = 'species';
   const resultsId = 'species-results';

   const fieldEl = ConsoleAutocompleteFieldBuilder.createAutocompleteField({
      label: 'Species',
      inputId,
      resultsId,
      placeholder: 'Search',
   });

   const inputEl = fieldEl.children[Position.SECOND];
   const resultsEl = fieldEl.children[Position.THIRD];
   assert.equal(inputEl.id, inputId);
   assert.equal(resultsEl.id, resultsId);
   assert.equal(resultsEl.className, 'console-operations-autocomplete');
});
