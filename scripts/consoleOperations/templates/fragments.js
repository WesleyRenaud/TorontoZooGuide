import { APP_STRINGS } from '../../strings.js';

function appendChild(parentEl, child) {
   if (!child) {
      return;
   }

   if (Array.isArray(child)) {
      child.forEach((item) => appendChild(parentEl, item));
      return;
   }

   parentEl.appendChild(child);
}

function appendChildren(parentEl, children = []) {
   children.forEach((child) => appendChild(parentEl, child));
   return parentEl;
}

function createFragment(children = []) {
   const fragment = document.createDocumentFragment();
   appendChildren(fragment, children);
   return fragment;
}

function createFieldWrapper() {
   const fieldEl = document.createElement('div');
   fieldEl.className = 'console-operations-field';
   return fieldEl;
}

function createLabel({
   text,
   htmlFor = '',
} = {}) {
   const labelEl = document.createElement('label');
   labelEl.className = 'console-operations-label';

   if (htmlFor) {
      labelEl.htmlFor = htmlFor;
   }

   labelEl.textContent = text;
   return labelEl;
}

function createOption({
   value = '',
   label,
} = {}) {
   const optionEl = document.createElement('option');
   optionEl.value = value;
   optionEl.textContent = label ?? value;
   return optionEl;
}

function createInput({
   inputId,
   type = 'text',
   className,
   placeholder = '',
   autocomplete = 'off',
   value = '',
} = {}) {
   const inputEl = document.createElement('input');
   inputEl.id = inputId;
   inputEl.type = type;
   inputEl.className = className;
   inputEl.autocomplete = autocomplete;

   if (placeholder) {
      inputEl.placeholder = placeholder;
   }

   if (value) {
      inputEl.value = value;
   }

   return inputEl;
}

function createHelpText(helpText = '') {
   if (!helpText) {
      return null;
   }

   const helpEl = document.createElement('div');
   helpEl.className = 'console-operations-help';
   helpEl.textContent = helpText;
   return helpEl;
}

export function createPanelShell({
   panelId,
   title,
   bodyChildren = [],
} = {}) {
   const panelEl = document.createElement('section');
   panelEl.id = panelId;
   panelEl.className = 'console-operations-panel';

   const headerEl = document.createElement('div');
   headerEl.className = 'console-operations-panel-header';

   const titleEl = document.createElement('h2');
   titleEl.className = 'console-operations-panel-title';
   titleEl.textContent = title;

   const bodyEl = document.createElement('div');
   bodyEl.className = 'console-operations-panel-body';

   headerEl.appendChild(titleEl);
   appendChildren(bodyEl, bodyChildren);
   panelEl.append(headerEl, bodyEl);

   return panelEl;
}

export function createSelectField({
   label,
   inputId,
   emptyOptionLabel,
   options = [],
   includeEmptyOption = true,
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
      htmlFor: inputId,
   });

   const selectEl = document.createElement('select');
   selectEl.id = inputId;
   selectEl.className = 'console-operations-input console-operations-select';

   if (includeEmptyOption) {
      selectEl.appendChild(createOption({
         value: '',
         label: emptyOptionLabel,
      }));
   }

   options.forEach((option) => {
      selectEl.appendChild(createOption(option));
   });

   fieldEl.append(labelEl, selectEl);
   return fieldEl;
}

export function createScheduleTimesCheckboxField({
   label,
   inputId,
   helpText = '',
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
   });

   const listEl = document.createElement('div');
   listEl.id = inputId;
   listEl.className = 'console-operations-schedule-times-list';

   const placeholderEl = document.createElement('div');
   placeholderEl.className = 'console-operations-schedule-times-placeholder';
   placeholderEl.textContent = APP_STRINGS.placeholders.selectWildEncounterFirst;

   listEl.appendChild(placeholderEl);
   fieldEl.append(labelEl, listEl);
   appendChild(fieldEl, createHelpText(helpText));

   return fieldEl;
}

export function createSchedulePresetField({
   inputId,
   label = APP_STRINGS.labels.schedulePreset,
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
      htmlFor: inputId,
   });

   const selectEl = document.createElement('select');
   selectEl.id = inputId;
   selectEl.className = 'console-operations-input console-operations-select';

   [
      { value: 'everyDay', label: APP_STRINGS.schedule.presetLabels.everyDay },
      { value: 'custom', label: APP_STRINGS.schedule.presetLabels.custom },
      { value: 'weekendsOnly', label: APP_STRINGS.schedule.presetLabels.weekendsOnly },
      { value: 'weekendsAndHolidays', label: APP_STRINGS.schedule.presetLabels.weekendsAndHolidays },
   ].forEach((option) => {
      selectEl.appendChild(createOption(option));
   });

   fieldEl.append(labelEl, selectEl);
   return fieldEl;
}

export function createTextInputField({
   label,
   inputId,
   placeholder,
   inputClass = 'console-operations-input',
   helpText = '',
   type = 'text',
   autocomplete = 'off',
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
      htmlFor: inputId,
   });

   const inputEl = createInput({
      inputId,
      type,
      className: inputClass,
      placeholder,
      autocomplete,
   });

   fieldEl.append(labelEl, inputEl);
   appendChild(fieldEl, createHelpText(helpText));

   return fieldEl;
}

export function createDateField({
   label,
   inputId,
   placeholder,
   helpText = '',
} = {}) {
   return createTextInputField({
      label,
      inputId,
      placeholder,
      helpText,
      inputClass: 'console-operations-input console-operations-datetime',
   });
}

export function createDateRangeFields({
   startDateId,
   startLabel = APP_STRINGS.labels.startDate,
   startPlaceholder = APP_STRINGS.placeholders.startDate,
   startHelpText = '',
   endDateId,
   endLabel = APP_STRINGS.labels.endDate,
   endPlaceholder = APP_STRINGS.placeholders.endDate,
   endHelpText = '',
} = {}) {
   return createFragment([
      createDateField({
         label: startLabel,
         inputId: startDateId,
         placeholder: startPlaceholder,
         helpText: startHelpText,
      }),
      createDateField({
         label: endLabel,
         inputId: endDateId,
         placeholder: endPlaceholder,
         helpText: endHelpText,
      }),
   ]);
}

export function createTextareaField({
   label,
   inputId,
   placeholder,
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
      htmlFor: inputId,
   });

   const textareaEl = document.createElement('textarea');
   textareaEl.id = inputId;
   textareaEl.className = 'console-operations-textarea';

   if (placeholder) {
      textareaEl.placeholder = placeholder;
   }

   fieldEl.append(labelEl, textareaEl);
   return fieldEl;
}

export function createAutocompleteField({
   label,
   inputId,
   resultsId,
   placeholder,
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
      htmlFor: inputId,
   });

   const inputEl = createInput({
      inputId,
      className: 'console-operations-input',
      placeholder,
      autocomplete: 'off',
   });

   const resultsEl = document.createElement('div');
   resultsEl.id = resultsId;
   resultsEl.className = 'console-operations-autocomplete';

   fieldEl.append(labelEl, inputEl, resultsEl);
   return fieldEl;
}

export function createCheckboxGridField({
   label,
   options = [],
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
   });

   const gridEl = document.createElement('div');
   gridEl.className = 'console-operations-checkbox-grid';

   options.forEach((option) => {
      const optionLabelEl = document.createElement('label');
      optionLabelEl.className = 'console-operations-checkbox-option';

      const inputEl = createInput({
         inputId: option.id,
         type: option.type || 'checkbox',
         className: '',
         autocomplete: '',
      });

      const textEl = document.createElement('span');
      textEl.textContent = option.label;

      optionLabelEl.append(inputEl, textEl);
      gridEl.appendChild(optionLabelEl);
   });

   fieldEl.append(labelEl, gridEl);
   return fieldEl;
}

export function createWeeklyScheduleCheckboxes({
   label = APP_STRINGS.labels.openOnTheseDays,
   dayIds = {},
   includeHolidays = true,
} = {}) {
   const options = [
      { id: dayIds.monday, label: APP_STRINGS.schedule.dayLabels.monday },
      { id: dayIds.tuesday, label: APP_STRINGS.schedule.dayLabels.tuesday },
      { id: dayIds.wednesday, label: APP_STRINGS.schedule.dayLabels.wednesday },
      { id: dayIds.thursday, label: APP_STRINGS.schedule.dayLabels.thursday },
      { id: dayIds.friday, label: APP_STRINGS.schedule.dayLabels.friday },
      { id: dayIds.saturday, label: APP_STRINGS.schedule.dayLabels.saturday },
      { id: dayIds.sunday, label: APP_STRINGS.schedule.dayLabels.sunday },
   ];

   if (includeHolidays && dayIds.holidays) {
      options.push({
         id: dayIds.holidays,
         label: APP_STRINGS.schedule.dayLabels.holidays,
      });
   }

   return createCheckboxGridField({
      label,
      options,
   });
}

export function createRadioGroupField({
   label,
   name,
   options = [],
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
   });

   const groupEl = document.createElement('div');
   groupEl.className = 'console-operations-radio-group';

   options.forEach((option) => {
      const optionLabelEl = document.createElement('label');
      optionLabelEl.className = 'console-operations-radio-option';

      const inputEl = createInput({
         inputId: option.id,
         type: 'radio',
         className: '',
         autocomplete: '',
         value: option.value,
      });
      inputEl.name = name;

      if (option.checked) {
         inputEl.checked = true;
      }

      const textEl = document.createElement('span');
      textEl.textContent = option.label;

      optionLabelEl.append(inputEl, textEl);
      groupEl.appendChild(optionLabelEl);
   });

   fieldEl.append(labelEl, groupEl);
   return fieldEl;
}

export function createActions({
   submitId,
   submitLabel = APP_STRINGS.actions.save,
} = {}) {
   const actionsEl = document.createElement('div');
   actionsEl.className = 'console-operations-actions';

   const submitButtonEl = document.createElement('button');
   submitButtonEl.id = submitId;
   submitButtonEl.type = 'button';
   submitButtonEl.className = 'console-operations-primary-btn';
   submitButtonEl.textContent = submitLabel;

   actionsEl.appendChild(submitButtonEl);
   return actionsEl;
}

export function createStatus({
   statusId,
} = {}) {
   const statusEl = document.createElement('div');
   statusEl.id = statusId;
   statusEl.className = 'console-operations-status';
   statusEl.setAttribute('aria-live', 'polite');
   return statusEl;
}

export function createMultiTimeField({
   label,
   listId,
   inputId,
   placeholder,
   helpText = '',
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
      htmlFor: inputId,
   });

   const compositeEl = document.createElement('div');
   compositeEl.className = 'console-operations-multi-time-field';

   const listEl = document.createElement('div');
   listEl.id = listId;
   listEl.className = 'console-operations-multi-time-list';

   const inputEl = createInput({
      inputId,
      className: 'console-operations-multi-time-input console-operations-datetime',
      placeholder,
   });

   compositeEl.append(listEl, inputEl);
   fieldEl.append(labelEl, compositeEl);
   appendChild(fieldEl, createHelpText(helpText));

   return fieldEl;
}

export function createWildEncounterScheduleRowsField({
   label = APP_STRINGS.labels.encounterTimes,
   rowsId,
   addRowButtonId,
   helpText = APP_STRINGS.help.encounterScheduleRows,
} = {}) {
   const fieldEl = createFieldWrapper();
   const labelEl = createLabel({
      text: label,
   });

   const rowsEl = document.createElement('div');
   rowsEl.id = rowsId;
   rowsEl.className = 'console-operations-schedule-rows';

   const addRowButtonEl = document.createElement('button');
   addRowButtonEl.id = addRowButtonId;
   addRowButtonEl.type = 'button';
   addRowButtonEl.className = 'console-operations-secondary-btn console-operations-schedule-rows-add';
   addRowButtonEl.textContent = APP_STRINGS.actions.addEncounterScheduleRow;

   fieldEl.append(labelEl, rowsEl, addRowButtonEl);
   appendChild(fieldEl, createHelpText(helpText));

   return fieldEl;
}
