import {
   createActionsHtml,
   createPanelShellHtml,
   createSelectFieldHtml,
   createStatusHtml,
} from '../../shared/panelFragments.js';

export function createZoomobileStationOpenPanelHtml() {
   return createPanelShellHtml({
      panelId: 'zoomobileStationOpenPanel',
      title: 'Set zoomobile station as open',
      bodyHtml: `
${createSelectFieldHtml({
   label: 'Zoomobile Station',
   inputId: 'zoomobileStationOpenZoomobileStation',
   emptyOptionLabel: 'Select a zoomobile station',
})}
${createActionsHtml({
   submitId: 'submitZoomobileStationOpen',
})}
${createStatusHtml({
   statusId: 'zoomobileStationOpenStatus',
})}
      `,
   });
}
