import { http, HttpResponse, delay } from "msw";
import { mockLatency } from "@/mocks/config";

const MOCK_REPLY = "Hello from the LiteLLM prototype playground. This response is mocked — no real API key required.";

function buildCompletionBody(content: string, model = "gpt-4o") {
  return {
    id: "chatcmpl-mock-prototype",
    object: "chat.completion",
    created: Math.floor(Date.now() / 1000),
    model,
    choices: [
      {
        index: 0,
        message: { role: "assistant", content },
        finish_reason: "stop",
      },
    ],
    usage: { prompt_tokens: 12, completion_tokens: 24, total_tokens: 36 },
  };
}

function streamChatCompletion(model: string): HttpResponse {
  const encoder = new TextEncoder();
  const words = MOCK_REPLY.split(" ");

  const stream = new ReadableStream({
    async start(controller) {
      await delay(mockLatency());
      for (const word of words) {
        const chunk = {
          id: "chatcmpl-mock-prototype",
          object: "chat.completion.chunk",
          model,
          choices: [{ index: 0, delta: { content: `${word} ` } }],
        };
        controller.enqueue(encoder.encode(`data: ${JSON.stringify(chunk)}\n\n`));
        await delay(60);
      }
      controller.enqueue(encoder.encode("data: [DONE]\n\n"));
      controller.close();
    },
  });

  return new HttpResponse(stream, {
    headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-cache" },
  });
}

export const playgroundHandlers = [
  http.post("*/v1/chat/completions", async ({ request }) => {
    let body: { stream?: boolean; model?: string } = {};
    try {
      body = (await request.json()) as typeof body;
    } catch {
      /* empty body */
    }
    const model = body.model ?? "gpt-4o";
    if (body.stream) {
      return streamChatCompletion(model);
    }
    await delay(mockLatency());
    return HttpResponse.json(buildCompletionBody(MOCK_REPLY, model));
  }),

  http.post("*/v1/embeddings", async () => {
    await delay(mockLatency());
    return HttpResponse.json({
      object: "list",
      data: [{ object: "embedding", index: 0, embedding: [0.1, 0.2, 0.3] }],
      model: "text-embedding-3-small",
      usage: { prompt_tokens: 4, total_tokens: 4 },
    });
  }),

  http.post("*/v1/responses", async () => {
    await delay(mockLatency());
    return HttpResponse.json({
      id: "resp_mock",
      output: [{ type: "message", content: [{ type: "text", text: MOCK_REPLY }] }],
    });
  }),

  http.post("*/utils/test_policies_and_guardrails", async () => {
    await delay(mockLatency());
    return HttpResponse.json({
      response: MOCK_REPLY,
      guardrail_errors: [],
    });
  }),
];
