import { createOffDisplayPanelHtml } from '../animals/panels/offDisplayPanel.js';
import { createOnDisplayPanelHtml } from '../animals/panels/onDisplayPanel.js';
import { createVisibilitySchedulePanelHtml } from '../animals/panels/visibilitySchedulePanel.js';
import { createRemoveVisibilitySchedulePanelHtml } from '../animals/panels/removeVisibilitySchedulePanel.js';
import { createViewingAlertPanelHtml } from '../animals/panels/viewingAlertPanel.js';
import { createRemoveViewingAlertPanelHtml } from '../animals/panels/removeViewingAlertPanel.js';

import { createExhibitClosedPanelHtml } from '../exhibits/panels/exhibitClosedPanel.js';
import { createExhibitOpenPanelHtml } from '../exhibits/panels/exhibitOpenPanel.js';

import { createRestaurantClosedPanelHtml } from '../restaurants/panels/restaurantClosedPanel.js';
import { createRestaurantOpenPanelHtml } from '../restaurants/panels/restaurantOpenPanel.js';

import { createGiftShopClosedPanelHtml } from '../giftShops/panels/giftShopClosedPanel.js';
import { createGiftShopOpenPanelHtml } from '../giftShops/panels/giftShopOpenPanel.js';

import { createAttractionClosedPanelHtml } from '../attractions/panels/attractionClosedPanel.js';
import { createAttractionOpenPanelHtml } from '../attractions/panels/attractionOpenPanel.js';

import { createZoomobileStationClosedPanelHtml } from '../zoomobile/panels/zoomobileStationClosedPanel.js';
import { createZoomobileStationOpenPanelHtml } from '../zoomobile/panels/zoomobileStationOpenPanel.js';
import { createZoomobileRoutePanelHtml } from '../zoomobile/panels/zoomobileRoutePanel.js';

import { createGuardiansTalkSchedulePanelHtml } from '../guardiansTalks/panels/guardiansTalkSchedulePanel.js';
import { createEndGuardiansTalkSchedulePanelHtml } from '../guardiansTalks/panels/endGuardiansTalkSchedulePanel.js';
import { createCancelGuardiansTalkOccurrencePanelHtml } from '../guardiansTalks/panels/cancelGuardiansTalkOccurrencePanel.js';

import { createWildEncounterSchedulePanelHtml } from '../wildEncounters/panels/wildEncounterSchedulePanel.js';
import { createEndWildEncounterSchedulePanelHtml } from '../wildEncounters/panels/endWildEncounterSchedulePanel.js';
import { createCancelWildEncounterOccurrencePanelHtml } from '../wildEncounters/panels/cancelWildEncounterOccurrencePanel.js';

const createPanelHtmlFns = [
   createOffDisplayPanelHtml,
   createOnDisplayPanelHtml,
   createVisibilitySchedulePanelHtml,
   createRemoveVisibilitySchedulePanelHtml,
   createViewingAlertPanelHtml,
   createRemoveViewingAlertPanelHtml,
   createExhibitClosedPanelHtml,
   createExhibitOpenPanelHtml,
   createRestaurantClosedPanelHtml,
   createRestaurantOpenPanelHtml,
   createGiftShopClosedPanelHtml,
   createGiftShopOpenPanelHtml,
   createAttractionClosedPanelHtml,
   createAttractionOpenPanelHtml,
   createZoomobileStationClosedPanelHtml,
   createZoomobileStationOpenPanelHtml,
   createZoomobileRoutePanelHtml,
   createGuardiansTalkSchedulePanelHtml,
   createEndGuardiansTalkSchedulePanelHtml,
   createCancelGuardiansTalkOccurrencePanelHtml,
   createWildEncounterSchedulePanelHtml,
   createEndWildEncounterSchedulePanelHtml,
   createCancelWildEncounterOccurrencePanelHtml,
];

function createConsoleOperationPanelsHtml() {
   return createPanelHtmlFns
      .map(createPanelHtml => createPanelHtml())
      .join('\n');
}

export function mountConsoleOperationPanels(workspaceEl) {
   if (!workspaceEl) {
      return;
   }

   workspaceEl.innerHTML = createConsoleOperationPanelsHtml();
}
