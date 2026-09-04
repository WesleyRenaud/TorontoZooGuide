import { APP_STRINGS } from '../../strings.js';
import { ScheduleConflictCompatibility } from '../wizard/scheduleConflictCompatibility.js';

export class ScheduleTimeConflictButtonState {
   static getConflictSelectionButtonState(
      selection,
      item,
      strings = APP_STRINGS
   ) {
      const selected = ScheduleConflictCompatibility.isConflictItemSelected(selection, item);
      const selectable = ScheduleConflictCompatibility.canSelectConflictItem(selection, item);
      const requiresTrimOverride = ScheduleConflictCompatibility.conflictItemRequiresTrimOverride(
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
