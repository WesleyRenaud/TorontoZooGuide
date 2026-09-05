import { showItineraryNoticePopup } from './components/noticePopup.js';
import { getItineraryPanelMountEl } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export class ShowScheduleItemNotice {
   static showScheduleItemNotice(message = '', deps = {}) {
      const {
         showNoticePopup = showItineraryNoticePopup,
         getMountEl = getItineraryPanelMountEl,
      } = deps;
      const strings = APP_STRINGS.itinerary;

      showNoticePopup({
         title: strings.scheduleItem.errorTitle,
         message,
         buttonText: strings.noItemsSelected.button,
         mountEl: getMountEl() ?? document.body,
      });
   }
}
