import assert from 'node:assert/strict';
import test from 'node:test';

import { SelectorShellBuilder } from '../../../../../scripts/itinerary/selectors/base/selectorShellBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_BuildSelectorShell_TestDefaults_ExpectShellParts', () => {
   const shell = SelectorShellBuilder.buildSelectorShell({
      topTitle: 'Builder',
      h1: 'Animals',
      subtitle: 'Pick animals',
   });

   assert.equal(shell.root.className, 'itin-overlay');
   assert.equal(shell.inputEl.placeholder, Strings.itinerary.searchPlaceholder);
   assert.equal(shell.nextButton.textContent, Strings.itinerary.actions.next);
   assert.equal(shell.finishButton.textContent, Strings.itinerary.actions.finish);
   assert.match(shell.root.textContent, /Animals/);
   assert.match(shell.root.textContent, /Pick animals/);
});

test('Test_BuildSelectorShell_TestHideNext_ExpectNullNext', () => {
   const shell = SelectorShellBuilder.buildSelectorShell({
      topTitle: 'Builder',
      h1: 'Done',
      subtitle: '',
      hideNextButton: true,
   });

   assert.equal(shell.nextButton, null);
   assert.equal(shell.finishButton.textContent, Strings.itinerary.actions.finish);
});
