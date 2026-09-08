import { ItineraryPanelFragment } from './components/itineraryPanelFragment.js';
import { NoticeFragment } from './components/noticeFragment.js';
import { Strings } from '../../strings.js';

export class ShowScheduleItemNoticeFragment {
   static showScheduleItemNotice(message = '', deps = {}) {
      const {
         showNoticePopup = NoticeFragment.showItineraryNoticePopup,
         getMountEl = ItineraryPanelFragment.getItineraryPanelMountEl,
      } = deps;
      showNoticePopup({
         title: Strings.itinerary.scheduleItem.errorTitle,
         message,
         buttonText: Strings.itinerary.noItemsSelected.button,
         mountEl: getMountEl() ?? document.body,
      });
   }
}
