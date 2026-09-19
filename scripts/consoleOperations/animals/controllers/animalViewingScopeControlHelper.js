import { ConsoleCheckboxGridFieldBuilder } from '../../templates/consoleCheckboxGridFieldBuilder.js';

export class AnimalViewingScopeControlHelper {
   static selectedEnclosureNames(gridEl) {
      return Array.from(gridEl.querySelectorAll('input[type="checkbox"]'))
         .filter((inputEl) => inputEl.checked)
         .map((inputEl) => inputEl.value);
   }


   static setFieldVisible(gridEl, isVisible) {
      gridEl?.closest('.console-operations-field')?.classList.toggle(
         'is-invisible',
         !isVisible
      );
   }


   static clearOptions(gridEl) {
      gridEl?.replaceChildren();
      AnimalViewingScopeControlHelper.setFieldVisible(gridEl, false);
   }


   static populateOptions(gridEl, scopes = [], {
      optionIdPrefix = 'viewingScope',
      isFieldVisible = scopes.length > 1,
   } = {}) {
      AnimalViewingScopeControlHelper.clearOptions(gridEl);

      scopes.forEach((scope, index) => {
         gridEl.appendChild(ConsoleCheckboxGridFieldBuilder.createCheckboxOption({
            id: `${optionIdPrefix}-${index}`,
            label: scope.label,
            value: scope.enclosureName,
            checked: true,
         }));
      });

      AnimalViewingScopeControlHelper.setFieldVisible(gridEl, isFieldVisible);
   }
}
