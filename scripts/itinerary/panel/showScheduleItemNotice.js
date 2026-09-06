import { NoticePopup } from './components/noticePopup.js';
import { Popup } from './components/popup.js';
import { Strings } from '../../strings.js';

export class ShowScheduleItemNotice {
   static showScheduleItemNotice(message = '', deps = {}) {
      const {
         showNoticePopup = NoticePopup.showItineraryNoticePopup,
         getMountEl = Popup.getItineraryPanelMountEl,
      } = deps;
      const strings = Strings.itinerary;

      showNoticePopup({
         title: strings.scheduleItem.errorTitle,
         message,
         buttonText: strings.noItemsSelected.button,
         mountEl: getMountEl() ?? document.body,
      });
   }
}
