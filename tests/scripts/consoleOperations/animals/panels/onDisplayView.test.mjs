import assert from 'node:assert/strict';
import test from 'node:test';

import { OnDisplayView } from '../../../../../scripts/consoleOperations/animals/panels/onDisplayView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleAutocompleteFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Strings } from '../../../../../scripts/strings.js';

test('Test_CreateOnDisplayPanel_TestWiring_ExpectShellOptions', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createAutocompleteField: ConsoleAutocompleteFieldBuilder.createAutocompleteField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };

   let captured;
   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return { panel: true };
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleAutocompleteFieldBuilder.createAutocompleteField = (options) => ({ kind: 'createAutocompleteField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = OnDisplayView.createOnDisplayPanel();

      assert.deepEqual(result, { panel: true });

      assert.equal(captured.panelId, 'onDisplayPanel');
      assert.equal(captured.title, Strings.panelTitles.onDisplay);
      assert.equal(captured.bodyChildren.length, 5);
      assert.equal(captured.bodyChildren[0].inputId, 'onDisplayExhibit');
      assert.equal(captured.bodyChildren[0].label, Strings.entityLabels.exhibit);
      assert.equal(captured.bodyChildren[1].inputId, 'onDisplaySpecies');
      assert.equal(captured.bodyChildren[1].resultsId, 'onDisplaySpeciesResults');
      assert.equal(captured.bodyChildren[1].label, Strings.labels.species);
      assert.equal(captured.bodyChildren[2].inputId, 'onDisplayViewingScope');
      assert.equal(captured.bodyChildren[2].label, Strings.labels.viewingScope);
      assert.equal(captured.bodyChildren[2].options, Strings.viewingScopes);
      assert.equal(captured.bodyChildren[3].submitId, 'submitOnDisplay');
      assert.equal(captured.bodyChildren[4].statusId, 'onDisplayStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleAutocompleteFieldBuilder.createAutocompleteField = originals.createAutocompleteField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
