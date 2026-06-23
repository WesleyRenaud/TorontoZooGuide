let pendingDayPlannerActionFeedback = null;

export function setPendingDayPlannerActionFeedback(feedback) {
   pendingDayPlannerActionFeedback = feedback;
}

export function consumePendingDayPlannerActionFeedback() {
   const feedback = pendingDayPlannerActionFeedback;
   pendingDayPlannerActionFeedback = null;
   return feedback;
}

export function resetPendingDayPlannerActionFeedback() {
   pendingDayPlannerActionFeedback = null;
}
