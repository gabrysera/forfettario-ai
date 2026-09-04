# Domain model

## Core entities

### TaxpayerProfile
Identity and fiscal facts relevant to the supported workflow. Identity data should be separated from rule-evaluation facts where possible.

### Activity
Human/business description of what the taxpayer does.

### ActivityClassification
ATECO version + code + confirmation/evidence status.

### TaxRegimeAssessment
Eligibility result for a specific period, containing condition-level outcomes and review status.

### SocialSecurityAssessment
Applicable social-security scheme/rate context for a specific period.

### Invoice
A fiscal/commercial document. An invoice is not itself proof that cash was collected.

### Payment
A cash event linked to an invoice when possible.

### OccasionalIncomeEvent
A separately modelled pre-/non-VAT work income event. Do not merge it into VAT-business invoice revenue.

### Obligation
A deadline/action that may require filing, payment or review.

### Calculation
Immutable calculation result containing input snapshot, ruleset version, formula components and timestamp.

### SourceReference
Reference to authoritative material supporting a rule.

## Important invariants

- `Invoice.issuedAt` and `Payment.receivedAt` are different concepts.
- tax-relevant revenue must be derived from the correct event type and applicable-period rules.
- occasional work income is not automatically VAT-business revenue.
- classification uncertainty is represented explicitly.
- a calculation is reproducible from stored inputs + ruleset version.
