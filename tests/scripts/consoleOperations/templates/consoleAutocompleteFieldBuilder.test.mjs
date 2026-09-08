import assert from 'node:assert/strict';
import test from 'node:test';

import { ConsoleAutocompleteFieldBuilder } from '../../../../scripts/consoleOperations/templates/consoleAutocompleteFieldBuilder.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_CreateAutocompleteField_TestConfig_ExpectInputAndResults', () => {
   const fieldEl = ConsoleAutocompleteFieldBuilder.createAutocompleteField({
      label: 'Species',
      inputId: 'species',
      resultsId: 'species-results',
      placeholder: 'Search',
   });
   assert.equal(fieldEl.children[1].id, 'species');
   assert.equal(fieldEl.children[2].id, 'species-results');
   assert.equal(fieldEl.children[2].className, 'console-operations-autocomplete');
});
