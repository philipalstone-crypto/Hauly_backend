# Alstone Hauly AI Backend

## Deploy on Render
1. Upload this folder to a GitHub repository.
2. In Render, create a **New Web Service** and connect the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add environment variable `OPENAI_API_KEY` in Render's Environment settings.
6. Optional: set `OPENAI_MODEL` to a model available to your OpenAI API project.
7. Set `FRONTEND_ORIGIN` to your website's exact origin, e.g. `https://example.netlify.app` (no trailing slash).

Never commit your real API key or put it in browser JavaScript.

## Test
Open `https://YOUR-RENDER-SERVICE.onrender.com/health`.
POST JSON to `/api/chat`:
```json
{"message":"Explain Python variables simply","history":[]}
```

## Frontend connection
```js
const response = await fetch("https://YOUR-RENDER-SERVICE.onrender.com/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: userMessage, history: chatHistory })
});
const data = await response.json();
if (!response.ok) throw new Error(data.error || "Request failed");
console.log(data.reply);
```

## Supabase database
This starter deliberately does not write to the database yet. Your existing `messages` table appears to use `conversation_id`, not `chat_id`. Before enabling database writes, inspect the actual `chats` and `messages` columns and confirm the foreign-key relationship so we don't damage or misconfigure existing data. Supabase URL/anon key should be configured only after adding authenticated-user verification and row-level security for the exact schema.
