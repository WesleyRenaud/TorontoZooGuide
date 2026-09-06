import { NoticePopup } from './components/noticePopup.js';
import { Popup } from './components/popup.js';
import { Strings } from '../../strings.js';

export class ShowScheduleItemNotice {
   static showScheduleItemNotice(message = '', deps = {}) {
      const {
         showNoticePopup = NoticePopup.showItineraryNoticePopup,
         getMountEl = Popup.getItineraryPanelMountEl,
      } = deps;
      showNoticePopup({
         title: Strings.itinerary.scheduleItem.errorTitle,
         message,
         buttonText: Strings.itinerary.noItemsSelected.button,
         mountEl: getMountEl() ?? document.body,
      });
   }
}
