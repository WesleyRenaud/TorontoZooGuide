import { NoticePopup } from './components/noticePopup.js';
import { Popup } from './components/popup.js';
import { APP_STRINGS } from '../../strings.js';

export class ShowScheduleItemNotice {
   static showScheduleItemNotice(message = '', deps = {}) {
      const {
         showNoticePopup = NoticePopup.showItineraryNoticePopup,
         getMountEl = Popup.getItineraryPanelMountEl,
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
