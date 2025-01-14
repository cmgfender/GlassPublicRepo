Prospecting Stage Automation

This repository provides a best-practice approach to handle multiple automation requirements related to Prospecting Stages in Salesforce. It consolidates logic into a single Apex handler class and uses one trigger per object—ensuring maintainability and avoiding recursion or conflicts.

Features
	1.	02-Detected
	•	When an AnonymizedAccount’s custom checkbox field (X6sense_CustomQA__c) flips from false to true, all related Opportunities have their Custom_Stage__c updated to "02-Detected".
	2.	03-Engaged
	•	When a AnonymizedMember record is inserted or updated with Status = 'Responded', the related Opportunities ([via AnonymizedOpportunityContactRole]) have their Custom_Stage__c updated to "03-Engaged".
	3.	04-Prioritized
	•	If an AnonymizedOpportunity has a roll-up or numeric field, CustomScore__c, that exceeds 100, the Custom_Stage__c is updated to "04-Prioritized"—unless it is already "05-Qualified".
	4.	05-Qualified
	•	When an AnonymizedOpportunity’s StageName changes to "Stage 1", it automatically updates the Custom_Stage__c to "05-Qualified".
	5.	Reverting Prospecting Stage
	•	Not included in a real-time trigger. A scheduled Apex/Flow must run daily (or as needed) to detect “No marketing engagement for 90 days” and revert the Custom_Stage__c to:
	•	"02-Detected" if AnonymizedAccount.X6sense_CustomQA__c = true
	•	"01-Targeted" if AnonymizedAccount.X6sense_CustomQA__c = false
	•	This logic is included as a stub method (revertProspectingStageAfter90Days()) in the handler class but is not invoked automatically.

File Structure

Below is the recommended folder/file structure:

.
├── README.md                                     # This file
├── classes
│   ├── AnonymizedHandler.cls     # Central handler class
│   ├── AnonymizedHandler.cls-meta.xml
│   ├── AnonymizedHandlerTest.cls        # Single test class
│   └── AnonymizedHandlerTest.cls-meta.xml
└── triggers
    ├── ProspectingStage_AnonymizedAccount.trigger
    ├── ProspectingStage_AnonymizedAccount.trigger-meta.xml
    ├── ProspectingStage_AnonymizedMember.trigger
    ├── ProspectingStage_AnonymizedMember.trigger-meta.xml
    ├── ProspectingStage_AnonymizedOpportunity.trigger
    └── ProspectingStage_AnonymizedOpportunity.trigger-meta.xml

1. AnonymizedHandler.cls
	•	Contains all business logic for the different Prospecting Stage updates:
	•	handleAnonymizedAccountUpdate(List<AnonymizedAccount>, Map<Id, AnonymizedAccount>)
	•	handleAnonymizedMember(List<AnonymizedMember>)
	•	handleAnonymizedOpportunityUpdate(List<AnonymizedOpportunity>, Map<Id, AnonymizedOpportunity>)
	•	Stub for revertProspectingStageAfter90Days() (Scheduled logic)

2. Triggers

Each trigger is extremely light, containing only a single call into the handler:
	•	ProspectingStage_AnonymizedAccount.trigger
	•	after update on AnonymizedAccount
	•	Invokes AnonymizedHandler.handleAnonymizedAccountUpdate(...)
	•	ProspectingStage_AnonymizedMember.trigger
	•	after insert, after update on AnonymizedMember
	•	Invokes AnonymizedHandler.handleAnonymizedMember(...)
	•	ProspectingStage_AnonymizedOpportunity.trigger
	•	after update on AnonymizedOpportunity
	•	Invokes AnonymizedHandler.handleAnonymizedOpportunityUpdate(...)

3. AnonymizedHandlerTest.cls
	•	Provides a single test class that covers:
	•	Flipping AnonymizedAccount.X6sense_CustomQA__c to true
	•	Inserting AnonymizedMember with Status='Responded'
	•	Updating AnonymizedOpportunity.CustomScore__c
	•	Changing AnonymizedOpportunity.StageName to 'Stage 1'
	•	Demonstrates end-to-end coverage of your triggers and logic.

Deployment

You can deploy these files into your Salesforce org using any of the following methods:
	1.	Salesforce CLI (SFDX)
	•	Place files in the correct force-app folder structure.
	•	Run sfdx force:source:deploy -p force-app/main/default (or similar).
	2.	Change Sets
	•	Create an Outbound Change Set in the source org, add these files, then deploy to the target org.
	3.	Developer Console
	•	Manually create the Apex Class, the Test Class, and each Trigger in Setup > Developer Console or Setup > Apex Classes/Triggers. Copy-paste the code from this repo into the respective files.

Usage & Behavior
	1.	02-Detected
	•	Update an AnonymizedAccount record’s X6sense_CustomQA__c from false to true.
	•	All related Opportunities will have Custom_Stage__c set to "02-Detected".
	2.	03-Engaged
	•	Insert or update a AnonymizedMember where Status = 'Responded'.
	•	All Opportunities linked to that Contact (via AnonymizedOpportunityContactRole) will have Custom_Stage__c set to "03-Engaged".
	3.	04-Prioritized
	•	If an AnonymizedOpportunity’s CustomScore__c is updated above 100, that Opp’s Custom_Stage__c becomes "04-Prioritized", unless it is already "05-Qualified".
	4.	05-Qualified
	•	Changing any AnonymizedOpportunity’s StageName to "Stage 1" immediately sets that Opp’s Custom_Stage__c to "05-Qualified".
	5.	Reversion
	•	Not triggered real-time; must be done via a Scheduled Apex or Scheduled Flow that calls AnonymizedHandler.revertProspectingStageAfter90Days() with the appropriate queries/updates.
	•	If X6sense_CustomQA__c is true, revert to "02-Detected"; otherwise revert to "01-Targeted".
	•	Do not revert if already "05-Qualified".

Testing
	•	Run the included AnonymizedHandlerTest in Setup > Apex Test Execution or in the Developer Console’s Test tab.
	•	You can also run sfdx force:apex:test:run -l RunLocalTests with the CLI.
	•	The test covers all relevant scenarios and ensures the triggers behave as intended.

Questions or Issues?
	•	Check the handler class for any custom field references (e.g., CustomScore__c, X6sense_CustomQA__c) that might need to be created in your org or renamed for your environment.
	•	If you need to handle the 90-day revert logic, see the revertProspectingStageAfter90Days() method stub in the handler class and implement a Schedulable class or Scheduled Flow that calls it.

Happy Automating!