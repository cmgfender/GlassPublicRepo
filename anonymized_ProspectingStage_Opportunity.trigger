/**
 * ProspectingStage_AnonymizedOpportunity.trigger
 *
 * Runs on AnonymizedOpportunity AFTER UPDATE,
 * delegates logic to the handler class.
 */
trigger ProspectingStage_AnonymizedOpportunity on AnonymizedOpportunity (after update) {
    AnonymizedHandler.handleAnonymizedOpportunityUpdate(Trigger.new, Trigger.oldMap);
}