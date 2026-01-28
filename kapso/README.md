# Kapso WhatsApp Integration

## Structure

```
kapso/
├── functions/           # Kapso function code (JS)
│   ├── resolve-user.js         # Phone → user lookup + KV cache
│   ├── route-by-role.js        # Decide node: route by user role
│   ├── fetch-teacher-subjects.js  # Format teacher subjects as text
│   ├── fetch-documents.js      # Format coordination documents as text
│   ├── relay-to-alizia.js      # Proxy chat to backend + KV history
│   └── get-area-teachers.js    # Get teachers with phone for an area
├── workflows/           # Kapso workflow graph definitions (JSON)
│   ├── main-router.json              # Entry point: resolve user, show menu
│   └── notify-document-published.json # Notify teachers on publish
└── templates/           # WhatsApp message templates
    └── document-published.json  # Notification template
```

## Deployment

### Prerequisites

- Kapso project with WhatsApp phone number connected
- Backend API accessible from Kapso (public URL or tunnel)

### Setup KV Config

Set the backend API URL in Kapso KV:
```
key: config:api_base_url
value: https://your-backend-url.com
```

### Deploy Functions

For each function in `functions/`:

```bash
cd .claude/skills/kapso-automation
node scripts/create-function.js --name <function-name> --code-file ../../../kapso/functions/<file>.js
node scripts/deploy-function.js --function-id <returned-id>
```

### Deploy Workflows

1. Create workflow: `node scripts/create-workflow.js --name main-router`
2. Update graph: `node scripts/update-graph.js <workflow_id> --expected-lock-version 0 --definition-file ../../../kapso/workflows/main-router.json`
3. Replace `FUNCTION_ID` placeholders with actual deployed function IDs
4. Create trigger: `node scripts/create-trigger.js <workflow_id> --trigger-type inbound_message --phone-number-id <id>`

### Create WhatsApp Template

```bash
cd .claude/skills/whatsapp-messaging
node scripts/create-template.mjs --business-account-id <WABA_ID> --file ../../../kapso/templates/document-published.json
```

### Backend Config

Set env var for the notification webhook:
```
KAPSO_WEBHOOK_URL=https://api.kapso.ai/platform/v1/projects/<PROJECT_ID>/workflows/<NOTIFY_WORKFLOW_ID>/trigger
```

## Flow

1. User sends WhatsApp message → `main-router` workflow triggers
2. `resolve-user` function looks up phone number via backend API
3. `route-by-role` decide node routes to coordinator or teacher menu
4. Interactive list menu shows options based on role
5. Selected action calls appropriate function (fetch docs, subjects, etc.)
6. On document publish from web → backend fires webhook → `notify-document-published` workflow sends template to area teachers
