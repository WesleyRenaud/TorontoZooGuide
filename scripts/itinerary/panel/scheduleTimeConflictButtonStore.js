import { Strings } from '../../strings.js';
import { ScheduleConflictChecker } from '../wizard/scheduleConflictChecker.js';

export class ScheduleTimeConflictButtonStore {
   static getConflictSelectionButtonState(
      selection,
      item,
      strings = Strings
   ) {
      const selected = ScheduleConflictChecker.isConflictItemSelected(selection, item);
      const selectable = ScheduleConflictChecker.canSelectConflictItem(selection, item);
      const requiresTrimOverride = ScheduleConflictChecker.conflictItemRequiresTrimOverride(
         selection,
         item
      );
      const aria = strings.itinerary.aria;

      return {
         selected,
         selectable,
         requiresTrimOverride,
         disabled: !selected && !selectable,
         textContent: selected
            ? strings.itinerary.actions.remove
            : strings.itinerary.actions.addSymbol,
         ariaLabel: selected
            ? (
               requiresTrimOverride
                  ? aria.removeFromItineraryWithScheduleOverride
                  : aria.removeFromItinerary
            )
            : (
               requiresTrimOverride
                  ? aria.addToItineraryWithScheduleOverride
                  : aria.addToItinerary
            ),
      };
   }

   static applyConflictSelectionButtonState(button, state) {
      button.disabled = state.disabled;
      button.classList.toggle('is-added', state.selected);
      button.classList.toggle(
         'requires-trim-override',
         state.requiresTrimOverride
      );
      button.textContent = state.textContent;
      button.setAttribute('aria-label', state.ariaLabel);
   }
}
