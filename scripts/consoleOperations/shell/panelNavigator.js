export function createConsolePanelNavigator(doc = document) {
   function activatePanel(panelEl) {
      doc
         .querySelectorAll('.console-operations-panel')
         .forEach(panel => panel.classList.remove('active'));

      panelEl?.classList.add('active');

      doc
         .querySelectorAll('.console-operations-menu-btn')
         .forEach(button => {
            button.classList.toggle(
               'active',
               button.dataset.panelTarget === panelEl?.id
            );
         });
   }

   function hidePanels() {
      doc
         .querySelectorAll('.console-operations-panel')
         .forEach(panel => panel.classList.remove('active'));

      doc
         .querySelectorAll('.console-operations-menu-btn')
         .forEach(button => button.classList.remove('active'));
   }

   return {
      activatePanel,
      hidePanels,
   };
}
