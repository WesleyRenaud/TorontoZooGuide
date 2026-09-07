import { PanelNavigator } from './panelNavigator.js';

export class PanelNavigatorUrlHelpers {
   static getDefaultLocation() {
      return globalThis.location ?? null;
   }

   static getDefaultHistory() {
      return globalThis.history ?? null;
   }

   static updateConsolePanelUrl(panelId, {
      location = PanelNavigatorUrlHelpers.getDefaultLocation(),
      history = PanelNavigatorUrlHelpers.getDefaultHistory(),
   } = {}) {
      if (!location || !history?.replaceState) {
         return;
      }

      const url = new URL(location.href);

      if (panelId) {
         url.searchParams.set(PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM, panelId);
      }
      else {
         url.searchParams.delete(PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM);
      }

      history.replaceState(null, '', url);
   }

   static getPanelIdFromUrl(location = getDefaultLocation()) {
      if (!location) {
         return '';
      }

      return new URL(location.href).searchParams.get(
         PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM
      ) ?? '';
   }

   static findMenuButtonForPanel(doc, panelId) {
      return Array.from(doc.querySelectorAll('.console-operations-menu-btn'))
         .find(button => button.dataset.panelTarget === panelId);
   }
}
