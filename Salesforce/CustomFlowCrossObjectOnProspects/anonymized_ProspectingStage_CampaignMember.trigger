/**
 * ProspectingStage_AnonymizedMember.trigger
 *
 * Runs on AnonymizedMember AFTER INSERT/UPDATE,
 * delegates logic to the handler class.
 */
trigger ProspectingStage_AnonymizedMember on AnonymizedMember (after insert, after update) {
    AnonymizedHandler.handleAnonymizedMember(Trigger.new);
}