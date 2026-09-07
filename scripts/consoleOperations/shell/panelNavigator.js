import { PanelNavigatorUrlHelpers } from './panelNavigatorUrlHelpers.js';
export class PanelNavigator {
   static ACTIVE_CONSOLE_PANEL_QUERY_PARAM = 'panel';

   static clearConsoleMenuButtonSelection(doc = document) {
      doc
         .querySelectorAll('.console-operations-menu-btn')
         .forEach(button => {
            button.classList.remove('active');
            button.removeAttribute('aria-current');
         });
   }

   static clearConsolePanelUrlParam(options = {}) {
      PanelNavigatorUrlHelpers.updateConsolePanelUrl('', options);
   }

   static createConsolePanelNavigator(
      doc = document,
      urlOptions = {}
   ) {
      function activatePanel(panelEl) {
         doc
            .querySelectorAll('.console-operations-panel')
            .forEach(panel => panel.classList.remove('active'));

         panelEl?.classList.add('active');
         PanelNavigatorUrlHelpers.updateConsolePanelUrl(panelEl?.id, urlOptions);

         doc
            .querySelectorAll('.console-operations-menu-btn')
            .forEach(button => {
               const isActive = button.dataset.panelTarget === panelEl?.id;

               button.classList.toggle('active', isActive);

               if (isActive) {
                  button.setAttribute('aria-current', 'page');
               }
               else {
                  button.removeAttribute('aria-current');
               }
            });
      }

      function hidePanels() {
         doc
            .querySelectorAll('.console-operations-panel')
            .forEach(panel => panel.classList.remove('active'));

         PanelNavigator.clearConsoleMenuButtonSelection(doc);

         PanelNavigator.clearConsolePanelUrlParam(urlOptions);
      }

      function restorePanelFromUrl() {
         const panelId = PanelNavigatorUrlHelpers.getPanelIdFromUrl(urlOptions.location);
         const button = PanelNavigatorUrlHelpers.findMenuButtonForPanel(doc, panelId);

         if (button) {
            button.click();
         }
      }

      return {
         activatePanel,
         hidePanels,
         restorePanelFromUrl,
      };
   }
}
