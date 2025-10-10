# CLO — Carbon Load Optimizer (MVP)

CLO reduces AI's carbon footprint by deciding **where**, **when**, and **how much** compute to use.
This MVP runs on Azure Functions (Python) and calls Azure OpenAI. Carbon signal is mocked for now.

## Endpoints
### POST /api/infer
Body:
```json
{
  "prompt": "Write a one-sentence update.",
  "priority": "P1",
  "allowDefer": true,
  "region": "eastus"
}
