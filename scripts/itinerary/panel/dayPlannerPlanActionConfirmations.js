import { showItineraryConfirmPopup } from './components/confirmPopup.js';
import { getItineraryDayPlannerViewMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

const STRINGS = APP_STRINGS.itinerary.dayPlanner;

function resolveDayPlannerConfirmationMountEl(mountEl) {
   return mountEl
      ?? getItineraryDayPlannerViewMountEl()
      ?? document.body;
}

export function showRebuildScheduleConfirmation({
   mountEl = null,
   onConfirm = null,
} = {}) {
   showItineraryConfirmPopup({
      title: STRINGS.rebuildScheduleTitle,
      message: STRINGS.rebuildScheduleMessage,
      confirmText: STRINGS.rebuildScheduleConfirm,
      cancelText: APP_STRINGS.itinerary.actions.cancel,
      mountEl: resolveDayPlannerConfirmationMountEl(mountEl),
      onConfirm,
   });
}
