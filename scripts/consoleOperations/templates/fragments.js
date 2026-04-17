function createHelpTextHtml(helpText = '') {
   if (!helpText) {
      return '';
   }

   return `
      <div class="console-operations-help">
         ${helpText}
      </div>
   `;
}

export function createPanelShellHtml({
   panelId,
   title,
   bodyHtml,
} = {}) {
   return `
      <section
         id="${panelId}"
         class="console-operations-panel"
      >

         <div class="console-operations-panel-header">
            <h2 class="console-operations-panel-title">
               ${title}
            </h2>
         </div>

         <div class="console-operations-panel-body">
${bodyHtml}
         </div>

      </section>
   `;
}

export function createSelectFieldHtml({
   label,
   inputId,
   emptyOptionLabel,
} = {}) {
   return `
            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="${inputId}"
               >
                  ${label}
               </label>

               <select
                  id="${inputId}"
                  class="console-operations-input console-operations-select"
               >
                  <option value="">${emptyOptionLabel}</option>
               </select>
            </div>
   `;
}

export function createSchedulePresetFieldHtml({
   inputId,
   label = 'Schedule preset',
} = {}) {
   return `
            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="${inputId}"
               >
                  ${label}
               </label>

               <select
                  id="${inputId}"
                  class="console-operations-input console-operations-select"
               >
                  <option value="everyDay">Every day</option>
                  <option value="custom">Custom</option>
                  <option value="weekendsOnly">Weekends only</option>
                  <option value="weekendsAndHolidays">Weekends + holidays only</option>
               </select>
            </div>
   `;
}

export function createTextInputFieldHtml({
   label,
   inputId,
   placeholder,
   inputClass = 'console-operations-input',
   helpText = '',
   type = 'text',
   autocomplete = 'off',
} = {}) {
   return `
            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="${inputId}"
               >
                  ${label}
               </label>

               <input
                  id="${inputId}"
                  type="${type}"
                  class="${inputClass}"
                  placeholder="${placeholder}"
                  autocomplete="${autocomplete}"
               >

${createHelpTextHtml(helpText)}
            </div>
   `;
}

export function createDateFieldHtml({
   label,
   inputId,
   placeholder,
   helpText = '',
} = {}) {
   return createTextInputFieldHtml({
      label,
      inputId,
      placeholder,
      helpText,
      inputClass: 'console-operations-input console-operations-datetime',
   });
}

export function createDateRangeFieldsHtml({
   startDateId,
   startLabel = 'Start date',
   startPlaceholder = 'Select a start date',
   startHelpText = '',
   endDateId,
   endLabel = 'End date',
   endPlaceholder = 'Select an end date',
   endHelpText = '',
} = {}) {
   return `
${createDateFieldHtml({
   label: startLabel,
   inputId: startDateId,
   placeholder: startPlaceholder,
   helpText: startHelpText,
})}
${createDateFieldHtml({
   label: endLabel,
   inputId: endDateId,
   placeholder: endPlaceholder,
   helpText: endHelpText,
})}
   `;
}

export function createTextareaFieldHtml({
   label,
   inputId,
   placeholder,
} = {}) {
   return `
            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="${inputId}"
               >
                  ${label}
               </label>

               <textarea
                  id="${inputId}"
                  class="console-operations-textarea"
                  placeholder="${placeholder}"
               ></textarea>
            </div>
   `;
}

export function createAutocompleteFieldHtml({
   label,
   inputId,
   resultsId,
   placeholder,
} = {}) {
   return `
            <div class="console-operations-field">
               <label
                  class="console-operations-label"
                  for="${inputId}"
               >
                  ${label}
               </label>

               <input
                  id="${inputId}"
                  type="text"
                  class="console-operations-input"
                  autocomplete="off"
                  placeholder="${placeholder}"
               >

               <div
                  id="${resultsId}"
                  class="console-operations-autocomplete"
               ></div>
            </div>
   `;
}

export function createCheckboxGridFieldHtml({
   label,
   options = [],
} = {}) {
   return `
            <div class="console-operations-field">
               <label class="console-operations-label">
                  ${label}
               </label>

               <div class="console-operations-checkbox-grid">
${options.map(option => `
                  <label class="console-operations-checkbox-option">
                     <input
                        id="${option.id}"
                        type="${option.type || 'checkbox'}"
                     >
                     <span>${option.label}</span>
                  </label>
`).join('')}
               </div>
            </div>
   `;
}

export function createWeeklyScheduleCheckboxesHtml({
   label = 'Open on these days',
   dayIds,
   includeHolidays = true,
} = {}) {
   const options = [
      { id: dayIds.monday, label: 'Monday' },
      { id: dayIds.tuesday, label: 'Tuesday' },
      { id: dayIds.wednesday, label: 'Wednesday' },
      { id: dayIds.thursday, label: 'Thursday' },
      { id: dayIds.friday, label: 'Friday' },
      { id: dayIds.saturday, label: 'Saturday' },
      { id: dayIds.sunday, label: 'Sunday' },
   ];

   if (includeHolidays && dayIds.holidays) {
      options.push({ id: dayIds.holidays, label: 'Holidays' });
   }

   return createCheckboxGridFieldHtml({
      label,
      options,
   });
}

export function createRadioGroupFieldHtml({
   label,
   name,
   options = [],
} = {}) {
   return `
            <div class="console-operations-field">
               <label class="console-operations-label">
                  ${label}
               </label>

               <div class="console-operations-radio-group">
${options.map(option => `
                  <label class="console-operations-radio-option">
                     <input
                        id="${option.id}"
                        name="${name}"
                        type="radio"
                        value="${option.value}"
                     >
                     <span>${option.label}</span>
                  </label>
`).join('')}
               </div>
            </div>
   `;
}

export function createActionsHtml({
   submitId,
   submitLabel = 'Save',
} = {}) {
   return `
            <div class="console-operations-actions">
               <button
                  id="${submitId}"
                  type="button"
                  class="console-operations-primary-btn"
               >
                  ${submitLabel}
               </button>
            </div>
   `;
}

export function createStatusHtml({
   statusId,
} = {}) {
   return `
            <div
               id="${statusId}"
               class="console-operations-status"
               aria-live="polite"
            ></div>
   `;
}
