export class ConsoleFieldPrimitiveBuilder {
   static appendChild(parentEl, child) {
      if (!child) {
         return;
      }

      if (Array.isArray(child)) {
         child.forEach((item) => ConsoleFieldPrimitiveBuilder.appendChild(parentEl, item));
         return;
      }

      parentEl.appendChild(child);
   }

   static appendChildren(parentEl, children = []) {
      children.forEach((child) => ConsoleFieldPrimitiveBuilder.appendChild(parentEl, child));
      return parentEl;
   }

   static createFragment(children = []) {
      const fragment = document.createDocumentFragment();
      ConsoleFieldPrimitiveBuilder.appendChildren(fragment, children);
      return fragment;
   }

   static createFieldWrapper() {
      const fieldEl = document.createElement('div');
      fieldEl.className = 'console-operations-field';
      return fieldEl;
   }

   static createLabel({
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

   static createOption({
      value = '',
      label,
   } = {}) {
      const optionEl = document.createElement('option');
      optionEl.value = value;
      optionEl.textContent = label ?? value;
      return optionEl;
   }

   static createInput({
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

   static createHelpText(helpText = '') {
      if (!helpText) {
         return null;
      }

      const helpEl = document.createElement('div');
      helpEl.className = 'console-operations-help';
      helpEl.textContent = helpText;
      return helpEl;
   }
}
