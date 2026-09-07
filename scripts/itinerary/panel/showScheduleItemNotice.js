import { ItineraryPanelPopup } from './components/itineraryPanelPopup.js';
import { NoticePopup } from './components/noticePopup.js';
import { Strings } from '../../strings.js';

export class ShowScheduleItemNotice {
   static showScheduleItemNotice(message = '', deps = {}) {
      const {
         showNoticePopup = NoticePopup.showItineraryNoticePopup,
         getMountEl = ItineraryPanelPopup.getItineraryPanelMountEl,
      } = deps;
      showNoticePopup({
         title: Strings.itinerary.scheduleItem.errorTitle,
         message,
         buttonText: Strings.itinerary.noItemsSelected.button,
         mountEl: getMountEl() ?? document.body,
      });
   }
}
