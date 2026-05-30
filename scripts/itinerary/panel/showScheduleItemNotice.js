import { showItineraryNoticePopup } from './components/noticePopup.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export function showScheduleItemNotice(message = '') {
   const strings = APP_STRINGS.itinerary;

   showItineraryNoticePopup({
      title: strings.scheduleItem.errorTitle,
      message,
      buttonText: strings.noItemsSelected.button,
      mountEl: getItineraryPanelMountEl() ?? document.body,
   });
}
