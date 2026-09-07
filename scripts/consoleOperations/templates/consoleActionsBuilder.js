import { Strings } from '../../strings.js';

export class ConsoleActionsBuilder {
   static createActions({
      submitId,
      submitLabel = Strings.actions.save,
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
}
