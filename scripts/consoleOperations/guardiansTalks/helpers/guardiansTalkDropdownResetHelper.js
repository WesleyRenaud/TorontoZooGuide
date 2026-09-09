import { ConsoleDropdownPopulator } from '../../options/consoleDropdownPopulator.js';

export class GuardiansTalkDropdownResetHelper {
   static resetTalkDropdown({
      talkNameEl,
      talkLocationFilterController = null,
   } = {}) {
      if (talkLocationFilterController?.clear) {
         talkLocationFilterController.clear();
         return;
      }

      if (talkNameEl?.tagName === 'SELECT') {
         ConsoleDropdownPopulator.populateGuardiansTalkDropdown(talkNameEl, []);
      }
      else if (talkNameEl) {
         talkNameEl.value = '';
      }
   }
}
