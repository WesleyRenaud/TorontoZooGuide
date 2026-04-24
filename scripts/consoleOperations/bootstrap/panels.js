import { createOffDisplayPanel } from '../animals/panels/offDisplayPanel.js';
import { createOnDisplayPanel } from '../animals/panels/onDisplayPanel.js';
import { createVisibilitySchedulePanel } from '../animals/panels/visibilitySchedulePanel.js';
import { createRemoveVisibilitySchedulePanel } from '../animals/panels/removeVisibilitySchedulePanel.js';
import { createViewingAlertPanel } from '../animals/panels/viewingAlertPanel.js';
import { createRemoveViewingAlertPanel } from '../animals/panels/removeViewingAlertPanel.js';
import { createExhibitClosedPanel } from '../exhibits/panels/exhibitClosedPanel.js';
import { createExhibitOpenPanel } from '../exhibits/panels/exhibitOpenPanel.js';
import { createRestaurantClosedPanel } from '../restaurants/panels/restaurantClosedPanel.js';
import { createRestaurantOpenPanel } from '../restaurants/panels/restaurantOpenPanel.js';
import { createGiftShopClosedPanel } from '../giftShops/panels/giftShopClosedPanel.js';
import { createGiftShopOpenPanel } from '../giftShops/panels/giftShopOpenPanel.js';
import { createAttractionClosedPanel } from '../attractions/panels/attractionClosedPanel.js';
import { createAttractionOpenPanel } from '../attractions/panels/attractionOpenPanel.js';
import { createZoomobileStationClosedPanel } from '../zoomobile/panels/zoomobileStationClosedPanel.js';
import { createZoomobileStationOpenPanel } from '../zoomobile/panels/zoomobileStationOpenPanel.js';
import { createZoomobileRoutePanel } from '../zoomobile/panels/zoomobileRoutePanel.js';
import { createGuardiansTalkSchedulePanel } from '../guardiansTalks/panels/guardiansTalkSchedulePanel.js';
import { createEndGuardiansTalkSchedulePanel } from '../guardiansTalks/panels/endGuardiansTalkSchedulePanel.js';
import { createCancelGuardiansTalkOccurrencePanel } from '../guardiansTalks/panels/cancelGuardiansTalkOccurrencePanel.js';
import { createWildEncounterSchedulePanel } from '../wildEncounters/panels/wildEncounterSchedulePanel.js';
import { createEndWildEncounterSchedulePanel } from '../wildEncounters/panels/endWildEncounterSchedulePanel.js';
import { createCancelWildEncounterOccurrencePanel } from '../wildEncounters/panels/cancelWildEncounterOccurrencePanel.js';

const PANEL_CREATORS = {
   animals: [
      createOffDisplayPanel,
      createOnDisplayPanel,
      createVisibilitySchedulePanel,
      createRemoveVisibilitySchedulePanel,
      createViewingAlertPanel,
      createRemoveViewingAlertPanel,
   ],
   exhibits: [
      createExhibitClosedPanel,
      createExhibitOpenPanel,
   ],
   restaurants: [
      createRestaurantClosedPanel,
      createRestaurantOpenPanel,
   ],
   giftShops: [
      createGiftShopClosedPanel,
      createGiftShopOpenPanel,
   ],
   attractions: [
      createAttractionClosedPanel,
      createAttractionOpenPanel,
   ],
   zoomobile: [
      createZoomobileStationClosedPanel,
      createZoomobileStationOpenPanel,
      createZoomobileRoutePanel,
   ],
   guardiansTalks: [
      createGuardiansTalkSchedulePanel,
      createEndGuardiansTalkSchedulePanel,
      createCancelGuardiansTalkOccurrencePanel,
   ],
   wildEncounters: [
      createWildEncounterSchedulePanel,
      createEndWildEncounterSchedulePanel,
      createCancelWildEncounterOccurrencePanel,
   ],
};

function getPanelCreators() {
   return Object.values(PANEL_CREATORS).flat();
}

function createConsoleOperationPanelsFragment(doc = document) {
   const fragment = doc.createDocumentFragment();

   getPanelCreators().forEach((createPanel) => {
      const panelEl = createPanel();
      fragment.appendChild(
         panelEl.ownerDocument === doc
            ? panelEl
            : doc.importNode(panelEl, true)
      );
   });

   return fragment;
}

export function mountConsoleOperationPanels(workspaceEl) {
   if (!workspaceEl) {
      return;
   }

   const doc = workspaceEl.ownerDocument || document;
   workspaceEl.replaceChildren(createConsoleOperationPanelsFragment(doc));
}
