import { describe, it, expect, beforeEach } from "vitest";
import { addKey, deleteKey, getKeysList, resetMockStore } from "@/mocks/mockStore";

describe("mockStore", () => {
  beforeEach(() => {
    resetMockStore();
  });

  it("should return initial keys", () => {
    expect(getKeysList().keys.length).toBeGreaterThanOrEqual(2);
  });

  it("should add and delete a key", () => {
    const before = getKeysList().total_count;
    addKey({ ...getKeysList().keys[0], token_id: "key-test", token: "sk-test" });
    expect(getKeysList().total_count).toBe(before + 1);
    deleteKey("key-test");
    expect(getKeysList().keys.find((k) => k.token_id === "key-test")).toBeUndefined();
  });
});
