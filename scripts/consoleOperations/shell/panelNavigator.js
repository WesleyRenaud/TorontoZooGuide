function getDefaultLocation() {
   return globalThis.location ?? null;
}

function getDefaultHistory() {
   return globalThis.history ?? null;
}

function updateConsolePanelUrl(panelId, {
   location = getDefaultLocation(),
   history = getDefaultHistory(),
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

function getPanelIdFromUrl(location = getDefaultLocation()) {
   if (!location) {
      return '';
   }

   return new URL(location.href).searchParams.get(
      PanelNavigator.ACTIVE_CONSOLE_PANEL_QUERY_PARAM
   ) ?? '';
}

function findMenuButtonForPanel(doc, panelId) {
   return Array.from(doc.querySelectorAll('.console-operations-menu-btn'))
      .find(button => button.dataset.panelTarget === panelId);
}

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
      updateConsolePanelUrl('', options);
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
         updateConsolePanelUrl(panelEl?.id, urlOptions);

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
         const panelId = getPanelIdFromUrl(urlOptions.location);
         const button = findMenuButtonForPanel(doc, panelId);

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
