# Human and Agent Rule Cross Reference

The same rule IDs apply to both versions. HUMAN_GUIDE.md simplifies language; FULL_GUIDANCE.md specifies behavior. Neither overrides the other silently. If their meaning differs, record the inconsistency and resolve it with the product policy owner before implementation.

Acceptance IDs refer to rows in ACCEPTANCE_CASES.md. They are requirements, not executed results.

| Rule | Human explanation | Full specification | Main acceptance coverage |
|---|---|---|---|
| R01 Purpose | [Purpose](HUMAN_GUIDE.md#r01-purpose) | [1 Purpose](FULL_GUIDANCE.md#1-purpose) | S09, G20 |
| R02 Setup and region | [First setup](HUMAN_GUIDE.md#r02-first-setup) | [3 Setup](FULL_GUIDANCE.md#3-region-setup-for-development-assistants), 27 Implementation inventory | S01–S02, R10 |
| R03 Scope and versions | [Versions](HUMAN_GUIDE.md#r03-first-and-second-versions) | [2 Scope](FULL_GUIDANCE.md#2-scope-and-versions) | S10–S11 |
| R04 Supporter journey | [Supporter](HUMAN_GUIDE.md#r04-a-supporter-wants-to-help) | [5 Supporter journey](FULL_GUIDANCE.md#5-supporter-journey) | S03–S09 |
| R05 Organization journey | [Organization](HUMAN_GUIDE.md#r05-an-organization-wants-its-information-checked) | [6 Organization review](FULL_GUIDANCE.md#6-organization-information-review-journey) | O01–O04 |
| R06 Qualification | [Six conditions](HUMAN_GUIDE.md#r06-when-a-case-can-be-recommended) | [7 Six gates](FULL_GUIDANCE.md#7-six-qualification-gates) | G01–G20 |
| R07 Evidence | [Evidence](HUMAN_GUIDE.md#r07-evidence) | [8 Evidence](FULL_GUIDANCE.md#8-evidence-standards) | G05–G07, R07, M04–M05, M14 |
| R08 Funding | [Funding](HUMAN_GUIDE.md#r08-funding) | [9 Funding](FULL_GUIDANCE.md#9-funding-calculations) | G08–G17 |
| R09 Risk channels | [Risk](HUMAN_GUIDE.md#r09-organization-risk) | [13 Risk](FULL_GUIDANCE.md#13-organization-risk-and-applicable-channels) | R01–R12 |
| R10 Freshness and updates | [Updates](HUMAN_GUIDE.md#r10-freshness-and-updates) | [11 Freshness](FULL_GUIDANCE.md#11-freshness-and-policy-configuration), [12 Updates](FULL_GUIDANCE.md#12-updates-caching-and-current-judgments) | H01–H16 |
| R11 Memory and history | [Memory](HUMAN_GUIDE.md#r11-memory-and-history) | [14 Feedback/memory](FULL_GUIDANCE.md#14-feedback-and-memory), [21 History](FULL_GUIDANCE.md#21-history-queries) | H12–H19, M19–M20 |
| R12 Tools and model authority | [Tools](HUMAN_GUIDE.md#r12-what-the-tools-do) | [16 Orchestration](FULL_GUIDANCE.md#16-evidence-driven-agent-system), [17 Models](FULL_GUIDANCE.md#17-model-responsibility-and-output-checks), [19 Adapters](FULL_GUIDANCE.md#19-adapter-contracts-and-connection-acceptance) | M04–M08, M15–M23, A01–A16 |
| R13 Credit and execution limits | [Credits](HUMAN_GUIDE.md#r13-efficient-use-and-demo-budget) | [18 Budgets](FULL_GUIDANCE.md#18-efficient-operation-and-budget-profiles) | M01–M03, M08–M13 |
| R14 Failures and trace | [Failures](HUMAN_GUIDE.md#r14-failures-and-visibility) | [20 Visibility](FULL_GUIDANCE.md#20-internal-review-user-visibility-and-run-records) | O05–O07, H09–H10, A11–A16 |
| R15 Permissions | [Permissions](HUMAN_GUIDE.md#r15-permissions-and-payments) | [10 Payments](FULL_GUIDANCE.md#10-no-payment-functionality), [15 Permissions](FULL_GUIDANCE.md#15-autonomous-permissions) | G18–G19, O08–O10 |
| R16 Human roles | [Responsibility](HUMAN_GUIDE.md#r16-human-responsibility) | [22 Business review](FULL_GUIDANCE.md#22-business-review-queue), [25 Handover](FULL_GUIDANCE.md#25-implementation-roles-and-handover) | R11–R12, A07–A10 |
| R17 Delivery evidence | [Working demo](HUMAN_GUIDE.md#r17-what-a-working-demo-must-show) | [26 Acceptance](FULL_GUIDANCE.md#26-acceptance-and-demonstration), [27 Inventory](FULL_GUIDANCE.md#27-implementation-inventory-and-delivery-evidence) | All cases, especially A01–A16, plus recorded minimum demonstration |

## Authority order

1. Applicable law/source access conditions and actual human-granted tool permissions.
2. Approved product policy and deployment settings within this specification.
3. This specification and its acceptance contracts.
4. Examples, which illustrate rather than authorize exceptions.

Unapproved choices remain open. The human companion is not a shortcut for ignoring a gate, and detailed engineering text cannot add a new product promise without review.
