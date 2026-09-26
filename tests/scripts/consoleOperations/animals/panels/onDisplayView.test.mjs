import assert from 'node:assert/strict';
import test from 'node:test';

import { OnDisplayView } from '../../../../../scripts/consoleOperations/animals/panels/onDisplayView.js';
import { ConsoleActionsBuilder } from '../../../../../scripts/consoleOperations/templates/consoleActionsBuilder.js';
import { ConsoleAutocompleteFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleAutocompleteFieldBuilder.js';
import { ConsoleCheckboxGridFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleCheckboxGridFieldBuilder.js';
import { ConsolePanelShellBuilder } from '../../../../../scripts/consoleOperations/templates/consolePanelShellBuilder.js';
import { ConsoleSelectFieldBuilder } from '../../../../../scripts/consoleOperations/templates/consoleSelectFieldBuilder.js';
import { ConsoleStatusBuilder } from '../../../../../scripts/consoleOperations/templates/consoleStatusBuilder.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../../scripts/strings.js';


test('Test_CreateOnDisplayPanel_TestWiring_ExpectShellOptions', () => {
   const originals = {
      createPanelShell: ConsolePanelShellBuilder.createPanelShell,
      createSelectField: ConsoleSelectFieldBuilder.createSelectField,
      createCheckboxGridField: ConsoleCheckboxGridFieldBuilder.createCheckboxGridField,
      createAutocompleteField: ConsoleAutocompleteFieldBuilder.createAutocompleteField,
      createActions: ConsoleActionsBuilder.createActions,
      createStatus: ConsoleStatusBuilder.createStatus,
   };
   const panel = { panel: true };
   let captured;

   ConsolePanelShellBuilder.createPanelShell = (options) => {
      captured = options;
      return panel;
   };
   ConsoleSelectFieldBuilder.createSelectField = (options) => ({ kind: 'createSelectField', ...options });
   ConsoleCheckboxGridFieldBuilder.createCheckboxGridField = (options) => ({ kind: 'createCheckboxGridField', ...options });
   ConsoleAutocompleteFieldBuilder.createAutocompleteField = (options) => ({ kind: 'createAutocompleteField', ...options });
   ConsoleActionsBuilder.createActions = (options) => ({ kind: 'createActions', ...options });
   ConsoleStatusBuilder.createStatus = (options) => ({ kind: 'createStatus', ...options });

   try {
      const result = OnDisplayView.createOnDisplayPanel();

      const exhibitField = captured.bodyChildren[Position.FIRST];
      const speciesField = captured.bodyChildren[Position.SECOND];
      const viewingScopeField = captured.bodyChildren[Position.THIRD];
      const actionsField = captured.bodyChildren[Position.FOURTH];
      const statusField = captured.bodyChildren.at(Position.LAST);
      assert.equal(result, panel);
      assert.equal(captured.panelId, 'onDisplayPanel');
      assert.equal(captured.title, Strings.panelTitles.onDisplay);
      assert.equal(exhibitField.inputId, 'onDisplayExhibit');
      assert.equal(exhibitField.label, Strings.entityLabels.exhibit);
      assert.equal(speciesField.inputId, 'onDisplaySpecies');
      assert.equal(speciesField.resultsId, 'onDisplaySpeciesResults');
      assert.equal(speciesField.label, Strings.labels.species);
      assert.equal(viewingScopeField.kind, 'createCheckboxGridField');
      assert.equal(viewingScopeField.label, Strings.labels.viewingScope);
      assert.equal(viewingScopeField.gridId, 'onDisplayViewingScope');
      assert.equal(actionsField.submitId, 'submitOnDisplay');
      assert.equal(statusField.statusId, 'onDisplayStatus');
   } finally {
      ConsolePanelShellBuilder.createPanelShell = originals.createPanelShell;
      ConsoleSelectFieldBuilder.createSelectField = originals.createSelectField;
      ConsoleCheckboxGridFieldBuilder.createCheckboxGridField = originals.createCheckboxGridField;
      ConsoleAutocompleteFieldBuilder.createAutocompleteField = originals.createAutocompleteField;
      ConsoleActionsBuilder.createActions = originals.createActions;
      ConsoleStatusBuilder.createStatus = originals.createStatus;
   }
});
