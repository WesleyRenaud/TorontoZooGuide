import { showItineraryNoticePopup } from './components/noticePopup.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export const BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME_ISSUE = (
   'bulkScheduleAnimalsNotEnoughTime'
);

export function hasBulkScheduleAnimalsNotEnoughTimeIssue(issues = []) {
   return issues.some(
      (issue) => issue?.type === BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME_ISSUE
   );
}

export function showBulkScheduleAnimalsNotEnoughTimeNotice({
   onConfirm = null,
   mountEl = getItineraryPanelMountEl() ?? document.body,
} = {}) {
   const strings = APP_STRINGS.itinerary.confirmation;

   showItineraryNoticePopup({
      title: strings.bulkScheduleAnimalsNotEnoughTimeTitle,
      message: strings.bulkScheduleAnimalsNotEnoughTimeMessage,
      buttonText: APP_STRINGS.itinerary.noItemsSelected.button,
      mountEl,
      onConfirm,
   });
}
