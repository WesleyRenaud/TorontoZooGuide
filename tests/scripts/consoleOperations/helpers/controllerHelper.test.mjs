import assert from 'node:assert/strict';
import test from 'node:test';

import { ControllerHelper } from '../../../../scripts/consoleOperations/helpers/controllerHelper.js';
import { PanelNavigator } from '../../../../scripts/consoleOperations/shell/panelNavigator.js';
import { Strings } from '../../../../scripts/strings.js';
import { VisitDateValidator } from '../../../../scripts/visitDates/visitDateValidator.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_ResetFieldValue_TestTextInput_ExpectCleared', () => {
   const text = document.createElement('input');
   text.value = 'hello';

   ControllerHelper.resetFieldValue(text);

   assert.equal(text.value, '');
});


test('Test_GetFieldValue_TestClearedInput_ExpectEmpty', () => {
   const text = document.createElement('input');
   text.value = 'hello';
   ControllerHelper.resetFieldValue(text);

   const value = ControllerHelper.getFieldValue(text);

   assert.equal(value, '');
});


test('Test_ResetFieldValue_TestCheckbox_ExpectUnchecked', () => {
   const checkbox = document.createElement('input');
   checkbox.type = 'checkbox';
   checkbox.checked = true;

   ControllerHelper.resetFieldValue(checkbox);

   assert.equal(checkbox.checked, false);
});


test('Test_ResetFieldValue_TestNull_ExpectNoThrow', () => {
   const fieldEl = null;

   assert.doesNotThrow(() => ControllerHelper.resetFieldValue(fieldEl));
});


test('Test_ResetFormFields_TestFields_ExpectCleared', () => {
   const text = document.createElement('input');
   text.value = 'x';
   const checkbox = document.createElement('input');
   checkbox.type = 'checkbox';
   checkbox.checked = true;

   ControllerHelper.resetFormFields([text, checkbox]);

   assert.equal(text.value, '');
   assert.equal(checkbox.checked, false);
});


test('Test_HasCheckedField_TestUnchecked_ExpectFalse', () => {
   const checkbox = document.createElement('input');
   checkbox.type = 'checkbox';
   checkbox.checked = false;

   const hasChecked = ControllerHelper.hasCheckedField([checkbox]);

   assert.equal(hasChecked, false);
});


test('Test_HasCheckedField_TestChecked_ExpectTrue', () => {
   const checkbox = document.createElement('input');
   checkbox.type = 'checkbox';
   checkbox.checked = true;

   const hasChecked = ControllerHelper.hasCheckedField([checkbox]);

   assert.equal(hasChecked, checkbox.checked);
});


test('Test_HideConsolePanel_TestActivePanel_ExpectCleared', () => {
   const statuses = [];
   const panelEl = document.createElement('div');
   panelEl.classList.add('active');
   const originalClearUrl = PanelNavigator.clearConsolePanelUrlParam;
   const originalClearMenu = PanelNavigator.clearConsoleMenuButtonSelection;
   const clears = [];
   PanelNavigator.clearConsolePanelUrlParam = () => {
      clears.push('url');
   };
   PanelNavigator.clearConsoleMenuButtonSelection = () => {
      clears.push('menu');
   };

   try {
      ControllerHelper.hideConsolePanel({
         panelEl,
         statusEl: {},
         setStatus: (_el, value) => {
            statuses.push(value);
         },
      });

      assert.equal(panelEl.classList.contains('active'), false);
      assert.deepEqual(clears, ['url', 'menu']);
      assert.deepEqual(statuses, ['']);
   } finally {
      PanelNavigator.clearConsolePanelUrlParam = originalClearUrl;
      PanelNavigator.clearConsoleMenuButtonSelection = originalClearMenu;
   }
});


test('Test_LoadOptionsAndShowPanel_TestSuccess_ExpectActivated', async () => {
   const options = ['a'];
   const panelEl = { id: 'panel' };
   const targetEl = {};
   const activations = [];

   await ControllerHelper.loadOptionsAndShowPanel({
      statusEl: {},
      setStatus: () => {},
      loadOptions: async () => options,
      populateOptions: (target, loaded) => {
         target.options = loaded;
      },
      targetEl,
      resetForm: () => {},
      activatePanel: (panel) => {
         activations.push(panel);
      },
      panelEl,
   });

   assert.deepEqual(activations, [panelEl]);
   assert.deepEqual(targetEl.options, options);
});


test('Test_LoadOptionsAndShowPanel_TestError_ExpectErrorStatus', async () => {
   const errorMessage = 'boom';
   const statuses = [];
   const activations = [];
   const panelEl = { id: 'err' };

   await ControllerHelper.loadOptionsAndShowPanel({
      statusEl: {},
      setStatus: (_el, value, tone) => {
         statuses.push({ value, tone });
      },
      loadOptions: async () => {
         throw new Error('fail');
      },
      activatePanel: (panel) => {
         activations.push(panel);
      },
      panelEl,
      errorMessage,
   });

   assert.deepEqual(activations, [panelEl]);
   assert.ok(statuses.some((entry) => entry.value === errorMessage && entry.tone === 'is-error'));
});


test('Test_ReloadOptions_TestLoadSucceeds_ExpectPopulatedAndReset', async () => {
   const exhibit = 'Africa Savanna';
   const loaded = [exhibit];
   const targetEl = { id: 'exhibit' };
   const populated = [];
   const resets = [];

   await ControllerHelper.reloadOptions({
      loadOptions: async () => loaded,
      populateOptions: (target, options) => {
         populated.push({ target, options });
      },
      targetEl,
      resetForm: () => {
         resets.push(true);
      },
   });

   assert.deepEqual(populated, [{ target: targetEl, options: loaded }]);
   assert.deepEqual(resets, [true]);
});


test('Test_ValidateOptionalDateRange_TestEmptyEnd_ExpectNull', () => {
   const original = VisitDateValidator.resolveOptionalStartDate;
   const startDate = '2026-06-15';
   VisitDateValidator.resolveOptionalStartDate = (value) => value || startDate;

   try {
      const message = ControllerHelper.validateOptionalDateRange(startDate, '');

      assert.equal(message, null);
   } finally {
      VisitDateValidator.resolveOptionalStartDate = original;
   }
});


test('Test_ValidateOptionalDateRange_TestEndBeforeStart_ExpectMessage', () => {
   const original = VisitDateValidator.resolveOptionalStartDate;
   const startDate = '2026-06-20';
   const endDate = '2026-06-10';
   VisitDateValidator.resolveOptionalStartDate = (value) => value || startDate;

   try {
      const message = ControllerHelper.validateOptionalDateRange(startDate, endDate);

      assert.equal(message, Strings.validation.endDateBeforeStartDate);
   } finally {
      VisitDateValidator.resolveOptionalStartDate = original;
   }
});


test('Test_ValidateOptionalDateRange_TestOrderedDates_ExpectNull', () => {
   const original = VisitDateValidator.resolveOptionalStartDate;
   const startDate = '2026-06-10';
   const endDate = '2026-06-20';
   VisitDateValidator.resolveOptionalStartDate = (value) => value || startDate;

   try {
      const message = ControllerHelper.validateOptionalDateRange(startDate, endDate);

      assert.equal(message, null);
   } finally {
      VisitDateValidator.resolveOptionalStartDate = original;
   }
});


test('Test_ValidateOptionalDateRange_TestInvalidDates_ExpectMessage', () => {
   const original = VisitDateValidator.resolveOptionalStartDate;
   const startDate = 'not-a-date';
   const endDate = 'also-bad';
   VisitDateValidator.resolveOptionalStartDate = (value) => value || startDate;

   try {
      const message = ControllerHelper.validateOptionalDateRange(startDate, endDate);

      assert.equal(message, Strings.validation.dateRangeInvalid);
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
