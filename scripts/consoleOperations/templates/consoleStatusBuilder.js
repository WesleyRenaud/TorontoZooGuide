export class ConsoleStatusBuilder {
   static createStatus({
      statusId,
   } = {}) {
      const statusEl = document.createElement('div');
      statusEl.id = statusId;
      statusEl.className = 'console-operations-status';
      statusEl.setAttribute('aria-live', 'polite');
      return statusEl;
   }
}
