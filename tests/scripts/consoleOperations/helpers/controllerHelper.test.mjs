import assert from 'node:assert/strict';
import test from 'node:test';

import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { PanelNavigator } from '../../../../scripts/consoleOperations/shell/panelNavigator.js';
import { Strings } from '../../../../scripts/strings.js';
import { VisitDateValidator } from '../../../../scripts/visitDates/visitDateValidator.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ResetAndGetFieldValue_TestInputTypes_ExpectCleared', () => {
   const text = document.createElement('input');
   text.value = 'hello';
   ControllerHelper.resetFieldValue(text);
   assert.equal(text.value, '');
   assert.equal(ControllerHelper.getFieldValue(text), '');

   const checkbox = document.createElement('input');
   checkbox.type = 'checkbox';
   checkbox.checked = true;
   ControllerHelper.resetFieldValue(checkbox);
   assert.equal(checkbox.checked, false);

   ControllerHelper.resetFieldValue(null);
});

test('Test_ResetFormFieldsAndHasCheckedField_TestFields_ExpectState', () => {
   const a = document.createElement('input');
   a.value = 'x';
   const b = document.createElement('input');
   b.type = 'checkbox';
   b.checked = true;

   ControllerHelper.resetFormFields([a, b]);
   assert.equal(a.value, '');
   assert.equal(b.checked, false);
   assert.equal(ControllerHelper.hasCheckedField([b]), false);
   b.checked = true;
   assert.equal(ControllerHelper.hasCheckedField([b]), true);
});

test('Test_HideConsolePanel_TestActivePanel_ExpectCleared', () => {
   const statuses = [];
   const panelEl = document.createElement('div');
   panelEl.classList.add('active');
   const originalClearUrl = PanelNavigator.clearConsolePanelUrlParam;
   const originalClearMenu = PanelNavigator.clearConsoleMenuButtonSelection;
   const clears = [];
   PanelNavigator.clearConsolePanelUrlParam = () => { clears.push('url'); };
   PanelNavigator.clearConsoleMenuButtonSelection = () => { clears.push('menu'); };

   try {
      ControllerHelper.hideConsolePanel({
         panelEl,
         statusEl: {},
         setStatus: (_el, value) => { statuses.push(value); },
      });
      assert.equal(panelEl.classList.contains('active'), false);
      assert.deepEqual(clears, ['url', 'menu']);
      assert.deepEqual(statuses, ['']);
   } finally {
      PanelNavigator.clearConsolePanelUrlParam = originalClearUrl;
      PanelNavigator.clearConsoleMenuButtonSelection = originalClearMenu;
   }
});

test('Test_LoadOptionsAndShowPanel_TestSuccessAndError_ExpectStatus', async () => {
   const statuses = [];
   const activations = [];

   await ControllerHelper.loadOptionsAndShowPanel({
      statusEl: {},
      setStatus: (_el, value, tone) => { statuses.push({ value, tone }); },
      loadOptions: async () => ['a'],
      populateOptions: (target, options) => { target.options = options; },
      targetEl: {},
      resetForm: () => {},
      activatePanel: (panel) => { activations.push(panel); },
      panelEl: { id: 'panel' },
   });

   assert.deepEqual(activations, [{ id: 'panel' }]);

   await ControllerHelper.loadOptionsAndShowPanel({
      statusEl: {},
      setStatus: (_el, value, tone) => { statuses.push({ value, tone }); },
      loadOptions: async () => { throw new Error('fail'); },
      activatePanel: (panel) => { activations.push(panel); },
      panelEl: { id: 'err' },
      errorMessage: 'boom',
   });

   assert.ok(statuses.some((entry) => entry.value === 'boom' && entry.tone === 'is-error'));
});

test('Test_ValidateOptionalDateRange_TestBounds_ExpectMessageOrNull', () => {
   const original = VisitDateValidator.resolveOptionalStartDate;
   VisitDateValidator.resolveOptionalStartDate = (value) => value || '2026-06-15';

   try {
      assert.equal(ControllerHelper.validateOptionalDateRange('2026-06-15', ''), null);
      assert.equal(
         ControllerHelper.validateOptionalDateRange('2026-06-20', '2026-06-10'),
         Strings.validation.endDateBeforeStartDate
      );
      assert.equal(ControllerHelper.validateOptionalDateRange('2026-06-10', '2026-06-20'), null);
   } finally {
      VisitDateValidator.resolveOptionalStartDate = original;
   }
});

test('Test_BindResetValueOnChange_TestChange_ExpectTargetReset', () => {
   const sourceEl = document.createElement('select');
   const targetEl = document.createElement('input');
   targetEl.value = 'keep';

   ControllerHelper.bindResetValueOnChange(sourceEl, targetEl);
   sourceEl.listeners.change();
   assert.equal(targetEl.value, '');
});
