export class SelectorShellBuilderHelper {
   static createButton({
      className,
      text,
      ariaLabel = null,
   } = {}) {
      const button = document.createElement('button');
      button.className = className;
      button.type = 'button';
      button.textContent = text;

      if (ariaLabel) {
         button.setAttribute('aria-label', ariaLabel);
      }

      return button;
   }
}
