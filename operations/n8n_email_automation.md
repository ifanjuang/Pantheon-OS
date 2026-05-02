# n8n email automation — operations note

> Operational note for future n8n email-triggered automations around Pantheon Next.
>
> This document does not install n8n, create workflows, define secrets or authorize production automation.

---

## 1. Doctrine

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
n8n déclenche ou notifie sous policy.
```

n8n is an external automation orchestrator. It may help with email triggers, webhooks, notifications and file handoff, but it must not become:

```text
Pantheon runtime
Pantheon scheduler
Pantheon approval authority
Pantheon memory
Pantheon source of truth
Hermes replacement
OpenWebUI replacement
```

---

## 2. Status

```yaml
tool: n8n
status: test
mode: local_sandbox_first
production_use: not_approved
source_of_truth: false
memory_authority: false
approval_authority: false
```

Reference policy:

```text
docs/governance/EXTERNAL_TOOLS_POLICY.md
```

---

## 3. Useful first use cases

Recommended first workflows are narrow and reversible.

### 3.1 Email received → operator notification

```text
email trigger
→ filter mailbox / label / sender / subject
→ create internal notification
→ no external reply
→ no memory write
```

Status:

```text
C3 local test
```

### 3.2 Email with attachment → controlled folder copy

```text
email trigger
→ detect attachment
→ save copy to controlled NAS folder
→ notify operator
→ no Knowledge ingestion yet
→ no memory write
```

Status:

```text
C3 local test
C4 if real project/client documents are involved
```

### 3.3 Email → candidate task note

```text
email trigger
→ extract metadata only
→ create candidate task note
→ operator validates in OpenWebUI
→ Hermes execution only after Task Contract
```

Status:

```text
C3 if internal
C4 if project/client data
```

### 3.4 Approved handoff → Hermes later

```text
validated candidate task
→ approved Task Contract
→ Hermes execution
→ Evidence Pack
→ OpenWebUI display
```

Status:

```text
future only
not implemented
```

---

## 4. Forbidden initial workflows

Do not create workflows that:

```text
automatically reply to clients or authorities
automatically send external emails
automatically create memory
automatically ingest documents into Knowledge
automatically trigger Hermes execution without Task Contract
automatically mutate Pantheon Markdown
automatically update STATUS.md / ROADMAP.md
automatically create PRs
automatically push to GitHub
automatically classify private project facts as reusable knowledge
```

External send is C4 minimum.

Secrets, broad filesystem access, Docker socket or public exposure are C5 or blocked.

---

## 5. Minimum sandbox deployment guardrails

Initial test deployment should be:

```text
local-only
not publicly exposed
behind authentication
no Docker socket
no broad host filesystem mount
no repository write mount
no private project data for first test
one connector at a time
one workflow per purpose
workflow disabled by default until reviewed
```

Secrets must be stored in n8n credential storage or deployment environment, never in the Pantheon repository.

---

## 6. Email connector guardrails

For email-triggered workflows:

```text
use a dedicated mailbox or label when possible
prefer metadata-only first pass
avoid full-body extraction in first test
avoid attachment processing until folder policy is defined
never commit raw email content to repo
never use email body as canonical memory
never send replies without human validation
```

Recommended metadata fields for candidate notes:

```yaml
email_candidate:
  received_at: string
  sender_domain: string
  subject_excerpt: string
  has_attachment: boolean
  attachment_count: integer
  mailbox_or_label: string
  proposed_domain: general | architecture_fr | software | unknown
  proposed_action: notify | classify | create_task_candidate | ignore
  privacy_assessment: public | internal | private | sensitive | unknown
  approval_required: C0 | C1 | C2 | C3 | C4 | C5
```

No real sender names, email addresses, client names, project names or addresses should be committed to the repo.

---

## 7. Handoff model

n8n may produce candidates.

Pantheon governs whether candidates become tasks.

Hermes executes only under Task Contract.

OpenWebUI exposes validation.

```text
Email event
→ n8n metadata/candidate workflow
→ OpenWebUI operator validation
→ Pantheon Task Contract candidate
→ approval if required
→ Hermes execution
→ Evidence Pack
→ optional memory candidate
```

---

## 8. Evidence requirements

Any n8n-triggered action that affects a project, document, client, external message or repository state must be traceable.

Minimum evidence fields:

```yaml
evidence_pack:
  trigger_source: n8n
  workflow_name: string
  workflow_version: string
  trigger_type: email | webhook | schedule | manual
  input_summary: string
  data_classes_seen: []
  actions_taken: []
  external_messages_sent: false
  files_created: []
  files_modified: []
  task_contract_ref: string | null
  approval_ref: string | null
  limitations: []
```

---

## 9. Suggested first test workflow

Use a fake/test mailbox and a synthetic email.

```text
Trigger: new email in test mailbox
Filter: subject contains [PANTHEON-TEST]
Action 1: create internal notification/log in n8n only
Action 2: no outbound email
Action 3: no file write except n8n execution log
Action 4: no Pantheon repo write
```

Pass criteria:

```text
workflow runs only on test mailbox
no external reply is sent
no secret is printed
no repo file is touched
no memory is written
operator can see the event and manually decide next step
```

---

## 10. Rollback

If n8n automation misbehaves:

```text
disable workflow
revoke connector credentials
rotate exposed credentials if needed
stop n8n container
remove webhook routes
review execution logs
create Evidence Pack if project/client data was involved
```

---

## 11. Open questions

```text
which mailbox or labels should be used for first test?
where should controlled attachment copies live on NAS?
which actions should stay notification-only?
which workflows require OpenWebUI validation?
what is the minimal Task Contract candidate format for email-triggered tasks?
```

---

## 12. Final rule

```text
n8n may detect and notify.
Pantheon decides.
Hermes executes.
OpenWebUI validates and displays.
```
