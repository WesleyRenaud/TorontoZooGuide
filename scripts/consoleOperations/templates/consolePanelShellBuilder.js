import { ConsoleFieldPrimitiveBuilder } from './consoleFieldPrimitiveBuilder.js';

export class ConsolePanelShellBuilder {
   static createPanelShell({
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
      ConsoleFieldPrimitiveBuilder.appendChildren(bodyEl, bodyChildren);
      panelEl.append(headerEl, bodyEl);

      return panelEl;
   }
}
